import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from mango.container.core import Container

from ..messages.codecs import Codec
from ..util.clock import ExternalClock
from ..util.termination_detection import tasks_complete_or_sleeping

logger = logging.getLogger(__name__)


@dataclass
class ExternalAgentMessage:
    message: bytes
    time: float
    receiver: str


@dataclass
class ExternalSchedulingContainerOutput:
    duration: float
    messages: List[ExternalAgentMessage]
    next_activity: Optional[float]


class ExternalSchedulingContainer(Container):
    """ """

    clock: ExternalClock  # type hint

    def __init__(
        self,
        *,
        addr: str,
        codec: Codec,
        loop: asyncio.AbstractEventLoop,
    ):
        """
        Initializes a ExternalSchedulingContainer. Do not directly call this method but use
        the factory method of **Container** instead
        :param addr: The container sid / eid respectively
        :param codec: The codec to use
        :param loop: Current event loop
        proto as codec
        """

        clock = ExternalClock()
        super().__init__(
            addr=addr,
            codec=codec,
            loop=loop,
            name=addr,
            clock=clock,
        )

        self.running = True
        self.current_start_time_of_step = time.time()
        self._new_internal_message: bool = False
        self.message_buffer = []

    async def send_message(
        self,
        content,
        receiver_addr: Union[str, Tuple[str, int]],
        *,
        receiver_id: Optional[str] = None,
        **kwargs,
    ) -> bool:
        """
        The Container sends a message to an agent according the container protocol.

        :param content: The content of the message
        :param receiver_addr: Address if the receiving container
        :param receiver_id: The agent id of the receiver
        :param kwargs: Additional parameters to provide protocol specific settings
        """
        message = content

        if receiver_addr == self.addr:
            if not receiver_id:
                receiver_id = message.receiver_id
            default_meta = {"network_protocol": "external_connection"}
            success = self._send_internal_message(
                message=message, receiver_id=receiver_id, default_meta=default_meta
            )
            self._new_internal_message = True
        else:
            success = await self._send_external_message(receiver_addr, message)

        return success

    async def _send_external_message(self, addr, message) -> bool:
        """
        Sends an external message to another container
        :param addr: The address of the receiving container
        :param message: The non-encoded message
        :return: Success or not
        """
        encoded_msg = self.codec.encode(message)
        # store message in the buffer, which will be emptied in step
        self.message_buffer.append(
            ExternalAgentMessage(
                time=time.time() - self.current_start_time_of_step + self.clock.time,
                receiver=addr,
                message=encoded_msg,
            )
        )
        return True

    async def step(
        self, simulation_time: float, incoming_messages: List[bytes]
    ) -> ExternalSchedulingContainerOutput:
        if self.message_buffer:
            logger.warning(
                "There are messages in teh message buffer to be sent, at the start when step was called."
            )

        self.current_start_time_of_step = time.time()

        self.clock.set_time(simulation_time)

        # now we will decode and distribute the incoming messages
        for encoded_msg in incoming_messages:
            message = self.codec.decode(encoded_msg)

            content, acl_meta = message.split_content_and_meta()
            acl_meta["network_protocol"] = "external_connection"

            await self.inbox.put((0, content, acl_meta))

        # now wait for the msg_queue to be empty
        await self.inbox.join()

        # now wait for all agents to terminate
        # we need to loop here, because we might need to join the agents inbox another times in case we send internal
        # messages
        while True:
            self._new_internal_message = False
            await tasks_complete_or_sleeping(self)
            # wait until all agents are done with their tasks
            if not self._new_internal_message:
                # if there have
                break
        # now all agents in this container should be done
        end_time = time.time()

        messages_this_step, self.message_buffer = self.message_buffer, []

        return ExternalSchedulingContainerOutput(
            duration=end_time - self.current_start_time_of_step,
            messages=messages_this_step,
            next_activity=self.clock.get_next_activity(),
        )

    async def shutdown(self):
        """
        calls shutdown() from super class Container
        """
        await super().shutdown()
