from schemas.command import Command
from client.executor import execute
import maya_tools.system_tools  # registers built-in tools


def run_command(data):
    command = Command.from_dict(data)
    return execute(command).to_dict()
