from typing import List, Optional, Any, Callable
from myko import MItem, Schema, AlertLevel, AlertEntityType, InstanceStatus, TargetStatus
from rship_sdk import ActionProps, EmitterProps, AlertProps


class Target(MItem):
    def __init__(self, id: str, name: str, action_ids: List[str], emitter_ids: List[str],
                 sub_targets: List[str], parent_targets: List[str], service_id: str,
                 bg_color: str, fg_color: str, last_updated: str, category: str, root_level: bool):
        super().__init__(id, name)
        self.action_ids = action_ids
        self.emitter_ids = emitter_ids
        self.sub_targets = sub_targets
        self.parent_targets = parent_targets
        self.service_id = service_id
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.last_updated = last_updated
        self.category = category
        self.root_level = root_level


class Action(MItem):
    def __init__(self, id: str, name: str, schema: Optional[Schema], target_id: str, service_id: str):
        super().__init__(id, name)
        self.schema = schema
        self.target_id = target_id
        self.service_id = service_id


class Emitter(MItem):
    def __init__(self, id: str, name: str, schema: Optional[Schema], target_id: str, service_id: str):
        super().__init__(id, name)
        self.schema = schema
        self.target_id = target_id
        self.service_id = service_id


class Pulse(MItem):
    def __init__(self, id: str, name: str, emitter_id: str, data: Any):
        super().__init__(id, name)
        self.emitter_id = emitter_id
        self.data = data


class Instance(MItem):
    def __init__(self, id: str, name: str, service_id: str, client_id: str, service_type_code: str,
                 status: InstanceStatus, machine_id: str, color: str):
        super().__init__(id, name)
        self.service_id = service_id
        self.client_id = client_id
        self.service_type_code = service_type_code
        self.status = status.value
        self.machine_id = machine_id
        self.color = color


class Machine(MItem):
    def __init__(self, id: str, name: str, dns_name: str, exec_name: str, address: str):
        super().__init__(id, name)
        self.dns_name = dns_name
        self.exec_name = exec_name
        self.address = address


class Alert(MItem):
    def __init__(self, id: str, entity_id: str, entity_type: AlertEntityType, instance_id: str,
                 level: AlertLevel, message: str, code: str):
        super().__init__(id, f"{entity_id}:{code}")
        self.entity_id = entity_id
        self.entity_type = entity_type.value
        self.instance_id = instance_id
        self.level = level.value
        self.message = message
        self.code = code


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
    def __init__(self, id: str, name: str, schema: Optional[Schema],
                 handler: Callable[[Action, Any], None]):
        self.id = id
        self.name = name
        self.schema = schema
        self.handler = handler

class EmitterProps:
    def __init__(self, id: str, name: str, schema: Optional[Schema]):
        self.id = id
        self.name = name
        self.schema = schema

class InstanceProps:
    def __init__(self, service_id: str, service_type_code: str, machine_id: str,
                 status: InstanceStatus, targets: List[TargetProps]):
        self.service_id = service_id
        self.service_type_code = service_type_code
        self.machine_id = machine_id
        self.status = status
        self.targets = targets