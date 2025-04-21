from mcp import ClientSession, types
from mcp.client.sse import sse_client
import asyncio

# This is a simple example client just utilized to test. The fast api server should already be running and this executed in a different session.

async def interact_with_mcp():
    print("Starting MCP client...")
    try:
        # Connect to the remote MCP server
        server_url = "http://127.0.0.1:8000/sse"  # SSE endpoint
        print(f"Connecting to MCP server at {server_url}...")
        
        # First establish the SSE connection
        async with sse_client(server_url) as (read, write):
            print("Connected to SSE endpoint")
            async with ClientSession(read, write) as session:
                print("Created client session")
                
                # Initialize the connection
                print("Initializing connection...")
                await session.initialize()
                print("Connection initialized")

                # 1. List available tools
                print("Listing tools...")
                tools = await session.list_tools()
                print("Available tools:", tools)

                # 2. Call the greet tool
                print("Calling get name tool...")
                result = await session.call_tool("get_user_name")
                print("Get name", result)

                """
                # 3. List available resources
                print("Listing resources...")
                resources = await session.list_resources()
                print("Available resources:", resources)

                # 4. Read the greeting resource
                print("Reading greeting resource...")
                content, mime_type = await session.read_resource("greeting://Alice")
                print("Greeting:", content)
                """
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(interact_with_mcp())
