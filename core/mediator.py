from typing import Dict, Type, Any
from core.interfaces.mediator import IMediator, IRequest, IRequestHandler

class Mediator(IMediator):
    def __init__(self):
        self._handlers: Dict[Type[IRequest], IRequestHandler] = {}

    def register_handler(self, request_type: Type[IRequest], handler: IRequestHandler):
        self._handlers[request_type] = handler

    async def send(self, request: IRequest[Any]) -> Any:
        handler = self._handlers.get(type(request))
        if not handler:
            raise ValueError(f"No handler registered for request type {type(request)}")
        return await handler.handle(request) 