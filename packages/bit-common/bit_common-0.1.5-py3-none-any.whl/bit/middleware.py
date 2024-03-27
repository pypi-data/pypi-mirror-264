from abc import ABC, abstractmethod
from typing import ParamSpec

from bit.model import BaseModel

P = ParamSpec("P")


class StopMiddlewareIteration(Exception):
    pass


class BaseMiddleware(ABC):
    @abstractmethod
    async def process_before(self, data: BaseModel) -> None:
        pass

    @abstractmethod
    async def process_after(self, data: BaseModel) -> None:
        pass
