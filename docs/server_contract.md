# 3DVPSserver ↔ Maya bootstrap contract

## User flow

1. User signs in to 3DVPSserver.
2. User activates an app, e.g. `maya_skin_tool`.
3. Server generates a short-lived bootstrap token.
4. User downloads one generated Python file based on `bootstrap/maya_app_loader.py`.
5. User drags the Python file into Maya.
6. Maya calls `onMayaDroppedPythonFile()`.
7. Bootstrap exchanges the token for a runtime session and app manifest.
8. Runtime files are written under Maya's user app directory and the manifest entrypoint is executed.

## Bootstrap generation

Replace these placeholders in `bootstrap/maya_app_loader.py` before download:

- `__SERVER_URL__`
- `__APP_ID__`
- `__BOOTSTRAP_TOKEN__`

Bootstrap tokens should be short-lived and preferably one-time use.

## POST /api/v1/maya/bootstrap/exchange

Request:

```json
{
  "app_id": "maya_skin_tool",
  "bootstrap_token": "short-lived-token",
  "client": "maya"
}
```

Response:

```json
{
  "session_token": "runtime-session-token",
  "granted_permissions": [
    "maya.scene.read",
    "maya.skin.write"
  ],
  "manifest": {
    "app_id": "maya_skin_tool",
    "name": "Maya Skin Tool",
    "version": "1.0.0",
    "entry_module": "maya_tools.skin_tool_app",
    "entry_function": "show",
    "permissions": [
      "maya.scene.read",
      "maya.skin.write"
    ]
  },
  "runtime_files": [
    {
      "path": "maya_tools/__init__.py",
      "content": ""
    },
    {
      "path": "maya_tools/skin_tool_app.py",
      "content": "..."
    }
  ]
}
```

## Security boundary

The server remains the authority for activation, session expiry, app permissions and runtime version. A Python file delivered to a user's machine cannot be treated as secret: users with local access can inspect code that is sent to Maya. Do not embed long-lived credentials or server secrets in bootstrap/runtime files.

Use short-lived bootstrap tokens, short-lived runtime sessions, server-side authorization, app/version manifests and revocation instead.

## Future endpoints

Suggested next endpoints:

- `GET /api/v1/apps/{app_id}/manifest`
- `POST /api/v1/maya/session/refresh`
- `POST /api/v1/maya/session/revoke`
- `POST /api/v1/maya/execute` for server-authorized remote commands when needed
- `POST /api/v1/maya/result` for task result/error reporting
