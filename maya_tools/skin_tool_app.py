from __future__ import print_function


WINDOW = "VPS_MayaSkinTool"


def _load_skinning():
    try:
        import NLTA_Skinning
        return NLTA_Skinning
    except Exception as exc:
        raise RuntimeError("NLTA_Skinning is not available: {}".format(exc))


def show(server_url=None, app_id=None, session_token=None, manifest=None):
    import maya.cmds as cmds

    if cmds.window(WINDOW, exists=True):
        cmds.deleteUI(WINDOW)

    manifest = manifest or {}
    window = cmds.window(WINDOW, title=manifest.get("name", "Maya Skin Tool"), sizeable=True)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=6)
    cmds.text(label="3DVPS Maya Skin Tool", align="center", height=28)
    cmds.separator(height=8, style="in")

    def run_fix_max(*_):
        skinning = _load_skinning()
        skinning.fixMaxInfluence()

    def run_unlock_two(*_):
        skinning = _load_skinning()
        skinning.UnlockTwoJoints()

    cmds.intField("maxInfluent", value=4, minValue=1)
    cmds.button(label="Fix Max Influence", command=run_fix_max)
    cmds.button(label="Unlock Two Joints", command=run_unlock_two)
    cmds.separator(height=8, style="in")
    cmds.text(label="App: {}".format(app_id or "maya_skin_tool"), align="left")

    cmds.showWindow(window)
    return window
