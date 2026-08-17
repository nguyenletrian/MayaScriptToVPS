from schemas.command import Command
from client.executor import execute
import maya_tools.system_tools  # registers built-in tools


def run_command(data):
    """Compatibility entrypoint for structured command execution."""
    command = Command.from_dict(data)
    return execute(command).to_dict()


def launch_app(entrypoint, server_url, app_id, session_token, manifest=None):
    """Development helper for launching a resolved app runtime inside Maya."""
    if not callable(entrypoint):
        raise RuntimeError("entrypoint must be callable")
    return entrypoint(
        server_url=server_url,
        app_id=app_id,
        session_token=session_token,
        manifest=manifest or {},
    )
