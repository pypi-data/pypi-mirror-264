from typing import Optional, Callable, Any, List
from myko import Schema

class ActionProps:
    def __init__(self, id: str, name: str, schema: Optional[Schema], handler: Callable[[Any], None]):
        self.id = id
        self.name = name
        self.schema = schema
        self.handler = handler

class EmitterProps:
    def __init__(self, id: str, name: str, schema: Optional[Schema]):
        self.id = id
        self.name = name
        self.schema = schema

class AlertProps:
    def __init__(self, message: str, level: str, code: str):
        self.message = message
        self.level = level
        self.code = code