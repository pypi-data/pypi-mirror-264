import asyncio
from libs.sdk.python.rship.src import RshipExecClient, Instance, Target, Action, Emitter, TargetProps, ActionProps, EmitterProps, InstanceProps
from myko import AlertLevel, InstanceStatus
from libs.sdk.python.rship.src.utils import get_current_timestamp

async def main():
    # Create an instance of RshipExecClient
    client = RshipExecClient("alpha.rship.io/myko")

    # Define a handler for incoming actions
    async def handle_action(action: Action, data: Any):
        print(f"Received action: {action.name}, Data: {data}")

    # Connect to the Rship server
    await client.connect()

    # Create an instance
    instance_props = InstanceProps(
        service_id="example-service",
        service_type_code="example-type",
        machine_id="example-machine",
        status=InstanceStatus.AVAILABLE,
        targets=[]
    )
    instance = Instance(
        id=f"{instance_props.machine_id}:{instance_props.service_id}",
        name=instance_props.service_id,
        **instance_props.__dict__
    )
    await client.set_data(instance)

    # Create a target
    target_props = TargetProps(
        id="example-target",
        name="Example Target",
        category="Test",
        actions=[],
        subtargets=[],
        parent_targets=[],
        emitters=[],
        alerts=[]
    )
    target = Target(
        id=f"{instance.service_id}:{target_props.id}",
        name=target_props.name,
        action_ids=[],
        emitter_ids=[],
        sub_targets=[],
        parent_targets=[],
        service_id=instance.service_id,
        bg_color="#ffffff",
        fg_color="#000000",
        last_updated=client.get_current_timestamp(),
        category=target_props.category,
        root_level=True
    )
    await client.save_target(target)

    # Create an action
    action_props = ActionProps(
        id="example-action",
        name="Example Action",
        schema=None,
        handler=handle_action
    )
    action = Action(
        id=f"{target.id}:{action_props.id}",
        name=action_props.name,
        schema=action_props.schema,
        target_id=target.id,
        service_id=instance.service_id
    )
    await client.save_action(action)
    client.save_handler(action.id, action_props.handler)

    # Create an emitter
    emitter_props = EmitterProps(
        id="example-emitter",
        name="Example Emitter",
        schema=None
    )
    emitter = Emitter(
        id=f"{target.id}:{emitter_props.id}",
        name=emitter_props.name,
        schema=emitter_props.schema,
        target_id=target.id,
        service_id=instance.service_id
    )
    await client.save_emitter(emitter)

    # Start receiving messages
    await client.receive_messages()

if __name__ == "__main__":
    asyncio.run(main())