from adapters.maya_adapter import get_maya_version
from registry.tool_registry import registry


def ping():
    return {"message": "pong", "maya_version": get_maya_version()}


registry.register("system.ping", ping, description="Check Maya executor availability", risk="low")
