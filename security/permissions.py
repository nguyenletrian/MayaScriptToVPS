class PermissionError(RuntimeError):
    pass


def require_permissions(granted, required):
    granted_set = set(granted or [])
    missing = [permission for permission in (required or []) if permission not in granted_set]
    if missing:
        raise PermissionError("Missing permissions: {}".format(", ".join(missing)))
    return True
