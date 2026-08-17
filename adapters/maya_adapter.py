def is_maya_available():
    try:
        import maya.cmds  # noqa: F401
        return True
    except Exception:
        return False


def get_maya_version():
    try:
        import maya.cmds as cmds
        return cmds.about(version=True)
    except Exception:
        return None
