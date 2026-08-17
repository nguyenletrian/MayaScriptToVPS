from schemas.result import Result
from registry.tool_registry import registry


def execute(command):
    tool_data = registry.get(command.tool)
    if not tool_data:
        return Result(False, error="Tool not registered: {}".format(command.tool), task_id=command.task_id)

    try:
        data = tool_data["func"](**command.args)
        return Result(True, data=data, task_id=command.task_id)
    except Exception as exc:
        return Result(False, error=str(exc), task_id=command.task_id)
