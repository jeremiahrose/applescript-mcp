import argparse
import logging
import json
from typing import Any, Dict, List, Optional
import os
import tempfile
import subprocess
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from pydantic import AnyUrl

logger = logging.getLogger('applescript_mcp')


def parse_arguments() -> argparse.Namespace:
    """Use argparse to allow values to be set as CLI switches
    or environment variables

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-level', default=os.environ.get('LOG_LEVEL', 'INFO'))
    return parser.parse_args()


def configure_logging():
    """Configure logging based on the log level argument"""
    args = parse_arguments()
    log_level = getattr(logging, args.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger.setLevel(log_level)
    logger.info(f"Logging configured with level: {args.log_level.upper()}")


async def main():
    """Run the AppleScript MCP server."""
    configure_logging()
    logger.info("Server starting")
    server = Server("applescript-mcp")

    @server.list_resources()
    async def handle_list_resources() -> list[types.Resource]:
        return []

    @server.read_resource()
    async def handle_read_resource(uri: AnyUrl) -> str:
        return ""

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="applescript_execute",
                description="""Run AppleScript code to interact with Mac applications and system features. This tool can access and manipulate data in Notes, Calendar, Contacts, Messages, Mail, Finder, Safari, and other Apple applications. Common use cases include but not limited to:
- Retrieve or create notes in Apple Notes
- Access or add calendar events and appointments
- List contacts or modify contact details
- Search for and organize files using Spotlight or Finder
- Get system information like battery status, disk space, or network details
- Read or organize browser bookmarks or history
- Access or send emails, messages, or other communications
- Read, write, or manage file contents
- Execute shell commands and capture the output
""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code_snippet": {
                            "type": "string",
                            "description": """Multi-line appleScript code to execute. """
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Command execution timeout in seconds (default: 60)"
                        }
                    },
                    "required": ["code_snippet"]
                },
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle execution of AppleScript to interact with Mac applications and data"""
        try:
            if name == "applescript_execute":
                if not arguments or "code_snippet" not in arguments:
                    raise ValueError("Missing code_snippet argument")

                # Get timeout parameter or use default
                timeout = arguments.get("timeout", 60)
                
                # Create temp file for the AppleScript
                with tempfile.NamedTemporaryFile(suffix='.scpt', delete=False) as temp:
                    temp_path = temp.name
                    try:
                        # Write the AppleScript to the temp file
                        temp.write(arguments["code_snippet"].encode('utf-8'))
                        temp.flush()
                        
                        # Execute the AppleScript
                        cmd = ["/usr/bin/osascript", temp_path]
                        result = subprocess.run(
                            cmd, 
                            capture_output=True, 
                            text=True, 
                            timeout=timeout
                        )
                        
                        if result.returncode != 0:
                            error_message = f"AppleScript execution failed: {result.stderr}"
                            return [types.TextContent(type="text", text=error_message)]
                        
                        return [types.TextContent(type="text", text=result.stdout)]
                    except subprocess.TimeoutExpired:
                        return [types.TextContent(type="text", text=f"AppleScript execution timed out after {timeout} seconds")]
                    except Exception as e:
                        return [types.TextContent(type="text", text=f"Error executing AppleScript: {str(e)}")]
                    finally:
                        # Clean up the temporary file
                        try:
                            os.unlink(temp_path)
                        except:
                            pass
            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="applescript-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
