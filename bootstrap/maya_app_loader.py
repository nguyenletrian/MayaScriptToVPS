"""Self-contained Maya drag/drop bootstrap template.

3DVPSserver should generate a copy of this file and replace:
    __SERVER_URL__
    __APP_ID__
    __BOOTSTRAP_TOKEN__

The bootstrap token should be short-lived and exchanged for a runtime session.
"""

from __future__ import print_function

import json
import os
import sys

try:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
except ImportError:  # Python 2 compatibility for older Maya installs.
    from urllib2 import Request, urlopen, HTTPError, URLError


SERVER_URL = "__SERVER_URL__".rstrip("/")
APP_ID = "__APP_ID__"
BOOTSTRAP_TOKEN = "__BOOTSTRAP_TOKEN__"
CLIENT_NAME = "maya"


def _request_json(path, payload=None, token=None, timeout=10):
    url = SERVER_URL + path
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = "Bearer " + token

    request = Request(url, data=body, headers=headers)
    try:
        response = urlopen(request, timeout=timeout)
        raw = response.read()
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace") if hasattr(exc, "read") else str(exc)
        raise RuntimeError("Server returned HTTP {}: {}".format(exc.code, detail))
    except URLError as exc:
        raise RuntimeError("Cannot connect to 3DVPSserver: {}".format(exc))

    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    return json.loads(raw) if raw else {}


def _exchange_bootstrap_token():
    return _request_json(
        "/api/v1/maya/bootstrap/exchange",
        {
            "app_id": APP_ID,
            "bootstrap_token": BOOTSTRAP_TOKEN,
            "client": CLIENT_NAME,
        },
    )


def _runtime_root():
    try:
        import maya.cmds as cmds
        root = cmds.internalVar(userAppDir=True)
    except Exception:
        root = os.path.expanduser("~")
    return os.path.join(root, "3DVPS", "runtime")


def _ensure_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    if path not in sys.path:
        sys.path.insert(0, path)


def _write_runtime_files(runtime_dir, files):
    for item in files:
        relative_path = item.get("path")
        content = item.get("content")
        if not relative_path or content is None:
            continue
        target = os.path.normpath(os.path.join(runtime_dir, relative_path))
        base = os.path.abspath(runtime_dir)
        if not os.path.abspath(target).startswith(base + os.sep):
            raise RuntimeError("Invalid runtime file path: {}".format(relative_path))
        folder = os.path.dirname(target)
        if not os.path.isdir(folder):
            os.makedirs(folder)
        with open(target, "wb") as stream:
            if not isinstance(content, bytes):
                content = content.encode("utf-8")
            stream.write(content)


def _load_entrypoint(runtime_dir, manifest):
    module_name = manifest.get("entry_module")
    function_name = manifest.get("entry_function", "show")
    if not module_name:
        raise RuntimeError("Manifest is missing entry_module")

    _ensure_path(runtime_dir)
    module = __import__(module_name, fromlist=[function_name])
    function = getattr(module, function_name, None)
    if not callable(function):
        raise RuntimeError("Entrypoint {}.{} is not callable".format(module_name, function_name))
    return function


def run():
    if not SERVER_URL or SERVER_URL.startswith("__"):
        raise RuntimeError("Bootstrap SERVER_URL has not been configured")
    if not APP_ID or APP_ID.startswith("__"):
        raise RuntimeError("Bootstrap APP_ID has not been configured")
    if not BOOTSTRAP_TOKEN or BOOTSTRAP_TOKEN.startswith("__"):
        raise RuntimeError("Bootstrap token is missing")

    session = _exchange_bootstrap_token()
    session_token = session.get("session_token")
    manifest = session.get("manifest") or {}
    runtime_files = session.get("runtime_files") or []

    if not session_token:
        raise RuntimeError("Server did not return a runtime session token")

    app_id = manifest.get("app_id") or APP_ID
    version = manifest.get("version") or "current"
    runtime_dir = os.path.join(_runtime_root(), app_id, version)
    _ensure_path(runtime_dir)
    _write_runtime_files(runtime_dir, runtime_files)

    entrypoint = _load_entrypoint(runtime_dir, manifest)
    return entrypoint(
        server_url=SERVER_URL,
        app_id=app_id,
        session_token=session_token,
        manifest=manifest,
    )


def onMayaDroppedPythonFile(*args):
    """Maya calls this automatically when the generated .py is dropped into Maya."""
    try:
        return run()
    except Exception as exc:
        try:
            import maya.cmds as cmds
            cmds.warning("3DVPS: {}".format(exc))
        except Exception:
            print("3DVPS: {}".format(exc))
        raise


if __name__ == "__main__":
    run()
