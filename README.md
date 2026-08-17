# MayaScriptToVPS

Bridge/executor layer between Maya tools and 3DVPSserver.

## Goal

Keep Maya execution isolated from the server. The server sends structured commands, this client resolves approved tools from a registry, executes them inside Maya, and returns structured results/errors.

## Planned flow

User/AI -> 3DVPSserver -> structured command -> MayaScriptToVPS -> ToolRegistry -> Maya tool -> result -> server

## Structure

- `client/`: connection, command handling, execution
- `registry/`: approved tool registry
- `schemas/`: command/result payload helpers
- `adapters/`: Maya/tool integration boundary
- `maya_tools/`: server-facing wrappers around Maya/NLTA functions

This repository intentionally does not copy the whole MayaScriptNew codebase. Existing NLTA modules remain the implementation library and can be wrapped gradually.
