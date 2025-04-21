from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


@mcp.tool()
async def get_user_name() -> str:
    """
    This function is used to retrieve the user name.
    """
    return "Joe"  # Note: this would be dynamically retrieved in an actual app

