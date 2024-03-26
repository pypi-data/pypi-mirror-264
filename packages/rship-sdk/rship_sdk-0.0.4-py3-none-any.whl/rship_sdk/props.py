from typing import Optional, Callable, Any
from myko import Schema

class TargetProps:
    def __init__(self, id: str, name: str, category: str, actions: List[ActionProps],
                 subtargets: List['TargetProps'], parent_targets: List[str],
                 emitters: List[EmitterProps], alerts: List[AlertProps]):
        self.id = id
        self.name = name
        self.category = category
        self.actions = actions
        self.subtargets = subtargets
        self.parent_targets = parent_targets
        self.emitters = emitters
        self.alerts = alerts

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