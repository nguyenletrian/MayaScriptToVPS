from __future__ import print_function

import json

try:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
except ImportError:
    from urllib2 import Request, urlopen, HTTPError, URLError


class APIClient(object):
    def __init__(self, server_url, session_token=None, timeout=10):
        self.server_url = server_url.rstrip("/")
        self.session_token = session_token
        self.timeout = timeout

    def request(self, path, payload=None, method=None):
        url = self.server_url + path
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {"Accept": "application/json"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        if self.session_token:
            headers["Authorization"] = "Bearer " + self.session_token

        request = Request(url, data=body, headers=headers)
        if method:
            request.get_method = lambda: method

        try:
            response = urlopen(request, timeout=self.timeout)
            raw = response.read()
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace") if hasattr(exc, "read") else str(exc)
            raise RuntimeError("HTTP {}: {}".format(exc.code, detail))
        except URLError as exc:
            raise RuntimeError("Connection failed: {}".format(exc))

        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        return json.loads(raw) if raw else {}

    def get_manifest(self, app_id):
        return self.request("/api/v1/apps/{}/manifest".format(app_id))

    def execute(self, app_id, tool, args=None, task_id=None):
        return self.request(
            "/api/v1/maya/execute",
            {
                "app_id": app_id,
                "tool": tool,
                "args": args or {},
                "task_id": task_id,
            },
        )
