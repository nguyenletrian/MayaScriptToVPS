from app.manifest import AppManifest
from security.permissions import require_permissions


def load_app(manifest_data, granted_permissions, entrypoint):
    manifest = AppManifest.from_dict(manifest_data).validate()
    require_permissions(granted_permissions, manifest.permissions)
    if not callable(entrypoint):
        raise RuntimeError("App entrypoint is not callable")
    return manifest
