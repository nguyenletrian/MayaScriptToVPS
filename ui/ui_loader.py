def close_window(window_name):
    try:
        import maya.cmds as cmds
    except Exception:
        return
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)


def show_message(title, message):
    import maya.cmds as cmds
    cmds.confirmDialog(title=title, message=message, button=["OK"])
