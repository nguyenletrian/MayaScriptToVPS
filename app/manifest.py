class AppManifest(object):
    def __init__(self, app_id, version, entry_module, entry_function="show", permissions=None, tools=None):
        self.app_id = app_id
        self.version = version
        self.entry_module = entry_module
        self.entry_function = entry_function
        self.permissions = permissions or []
        self.tools = tools or []

    @classmethod
    def from_dict(cls, data):
        return cls(
            app_id=data.get("app_id"),
            version=data.get("version", "current"),
            entry_module=data.get("entry_module"),
            entry_function=data.get("entry_function", "show"),
            permissions=data.get("permissions") or [],
            tools=data.get("tools") or [],
        )

    def validate(self):
        if not self.app_id:
            raise ValueError("manifest.app_id is required")
        if not self.entry_module:
            raise ValueError("manifest.entry_module is required")
        return self
