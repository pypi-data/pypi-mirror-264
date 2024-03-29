import asyncio
import typing
from functools import wraps
from typing import Any, Callable, Concatenate, Coroutine, ParamSpec, Union, cast

from bit.type.bitarray import BitArray

if typing.TYPE_CHECKING:
    from bit.controller import BaseController


P = ParamSpec("P")


def create_task(
    func: Callable[Concatenate["BaseProtocol", P], Coroutine[Any, Any, None]],
) -> Callable[Concatenate["BaseProtocol", P], None]:
    """Decorator to create a task from a coroutine.

    Nothing can be returned from the decorated function.
    """

    @wraps(func)
    def wrapper(cls_or_self: "BaseProtocol", /, *args: P.args, **kwargs: P.kwargs) -> None:
        coro = func(cls_or_self, *args, **kwargs)
        asyncio.create_task(coro)

    return wrapper


class BaseProtocol(asyncio.BaseProtocol):
    def __init__(self, controller: "BaseController") -> None:
        self.transport: Union[
            asyncio.BaseTransport,
            asyncio.Transport,
            asyncio.DatagramTransport,
            None,
        ] = None

        self.controller = controller

    @create_task
    async def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport = transport

        await self.controller.new_connection(transport)

    @create_task
    async def data_received(self, data: bytes) -> None:
        """Called when some TCP data is received."""

        self.transport = cast(asyncio.Transport, self.transport)

        result = await self.handle_data(data)

        if result is not None:
            self.transport.write(result)

    async def datagram_received(self, data: bytes, addr: Any) -> None:
        """Called when some datagram is received."""

        self.transport = cast(asyncio.DatagramTransport, self.transport)

        result = await self.handle_data(data)

        if result is not None:
            self.transport.sendto(result, addr)

    async def handle_data(self, data: bytes) -> bytes | None:
        """Handle incoming data."""

        data_model = await self.controller.convert_data(data)

        result = await self.controller.process(data_model)

        if result is not None:
            return BitArray.bits_to_bytes(result.to_bits())

        return None

    @create_task
    async def connection_lost(self, exc: Exception | None) -> None:
        await self.controller.connection_lost(exc)
