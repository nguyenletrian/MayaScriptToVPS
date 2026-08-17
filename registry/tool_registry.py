class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, func, description="", permission="maya", risk="low"):
        self._tools[name] = {"func": func, "description": description, "permission": permission, "risk": risk}
        return func

    def unregister(self, name):
        self._tools.pop(name, None)

    def get(self, name):
        return self._tools.get(name)

    def has(self, name):
        return name in self._tools

    def list_tools(self):
        return {name: {k: v for k, v in data.items() if k != "func"} for name, data in self._tools.items()}


registry = ToolRegistry()
