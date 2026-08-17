class Command:
    def __init__(self, tool, args=None, task_id=None):
        self.tool = tool
        self.args = args or {}
        self.task_id = task_id

    @classmethod
    def from_dict(cls, data):
        return cls(tool=data.get("tool"), args=data.get("args") or {}, task_id=data.get("task_id"))

    def to_dict(self):
        return {"tool": self.tool, "args": self.args, "task_id": self.task_id}
