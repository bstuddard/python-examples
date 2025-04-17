from src.build_mcp.create_mcp import *
from src.startup.app import app
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount
from fastapi import Request


# Mount to fastapi app
sse = SseServerTransport("/messages/")
app.router.routes.append(Mount("/messages", app=sse.handle_post_message))

# Add routes for sse
@app.get('/sse')
async def handle_sse(request: Request) -> None:
    # See https://github.com/modelcontextprotocol/python-sdk/blob/main/src/mcp/server/fastmcp/server.py for more details
    async with sse.connect_sse(
        request.scope,
        request.receive,
        request._send,  # type: ignore[reportPrivateUsage]
    ) as streams:
        await mcp._mcp_server.run(
            streams[0],
            streams[1],
            mcp._mcp_server.create_initialization_options(),
        )