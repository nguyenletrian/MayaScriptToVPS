class Result:
    def __init__(self, success, data=None, error=None, task_id=None):
        self.success = success
        self.data = data
        self.error = error
        self.task_id = task_id

    def to_dict(self):
        return {"success": self.success, "data": self.data, "error": self.error, "task_id": self.task_id}
