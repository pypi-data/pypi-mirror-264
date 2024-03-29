import typing
from abc import ABC, abstractmethod
from asyncio.transports import BaseTransport, DatagramTransport, Transport
from typing import ClassVar, ParamSpec

from bit.model import BaseModel
from bit.type.bitarray import BitArray

if typing.TYPE_CHECKING:
    from bit.middleware import BaseMiddleware, StopMiddlewareIteration

P = ParamSpec("P")


class BaseController(ABC):
    MESSAGE_TYPE: ClassVar[type[BaseModel]]

    def __init__(self, middleware: list["BaseMiddleware"] | None = None) -> None:
        self.middleware = middleware or []

    async def new_connection(
        self,
        transport: BaseTransport | DatagramTransport | Transport,
    ) -> None:
        pass

    async def connection_lost(self, exc: Exception | None) -> None:
        pass

    @abstractmethod
    async def handle(self, data: BaseModel, *args: P.args, **kwargs: P.kwargs) -> BaseModel:
        pass

    async def convert_data(self, data: bytes) -> BaseModel:
        """Convert data to message type."""

        bits = BitArray.bytes_to_bits(data)

        return self.MESSAGE_TYPE.from_bits(bits)

    async def process(self, data: BaseModel) -> BaseModel:
        """Process data with middleware."""

        for middleware in self.middleware:
            try:
                await middleware.process_before(data)
            except StopMiddlewareIteration:
                break

        result = await self.handle(data)

        for middleware in self.middleware:
            try:
                await middleware.process_after(result)
            except StopMiddlewareIteration:
                break

        return result
