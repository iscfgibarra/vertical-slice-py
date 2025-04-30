from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

TResponse = TypeVar('TResponse')

class IRequest(Generic[TResponse], ABC):
    pass

class IRequestHandler(Generic[TResponse], ABC):
    @abstractmethod
    async def handle(self, request: IRequest[TResponse]) -> TResponse:
        pass

class IMediator(ABC):
    @abstractmethod
    async def send(self, request: IRequest[Any]) -> Any:
        pass 