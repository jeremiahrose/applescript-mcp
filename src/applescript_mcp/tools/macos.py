"""macOS system-level tools for window management, system information, and AppleScript execution."""

import mcp.types as types
from typing import List, Dict, Any
from ..utils.applescript import execute_applescript


def get_tools() -> List[types.Tool]:
    """Return list of macOS tool definitions."""
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
                            "description": "Multi-line AppleScript code to execute"
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Command execution timeout in seconds (default: 60)"
                        }
                    },
                    "required": ["code_snippet"],
                    "additionalProperties": False
                }
            ),
            types.Tool(
                name="get_screen_resolution",
                description="Get the current screen resolution and display information",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            ),
            types.Tool(
                name="foreground_window",
                description="Bring a window of the specified application to the foreground",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "app_name": {
                            "type": "string",
                            "description": "Name of the application to bring to foreground"
                        }
                    },
                    "required": ["app_name"],
                    "additionalProperties": False
                }
            ),
            types.Tool(
                name="dock_window_horizontal",
                description="Dock a window horizontally using percentage bounds (e.g., 0,50 for left half, 50,100 for right half)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "app_name": {
                            "type": "string",
                            "description": "Application name to dock"
                        },
                        "left_percent": {
                            "type": "number",
                            "description": "Left edge as percentage of screen width (0-100)"
                        },
                        "right_percent": {
                            "type": "number",
                            "description": "Right edge as percentage of screen width (0-100)"
                        }
                    },
                    "required": ["app_name", "left_percent", "right_percent"],
                    "additionalProperties": False
                }
            ),
            types.Tool(
                name="get_window_info",
                description="Get information about the frontmost window including position and size",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "app_name": {
                            "type": "string",
                            "description": "Optional: specific application name to get info for"
                        }
                    },
                    "additionalProperties": False
                }
            ),
            types.Tool(
                name="get_system_info",
                description="Get basic system information including macOS version, computer name, and memory",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            )
        ]

async def handle_tool_call(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle macOS tool calls."""
    try:
        if name == "applescript_execute":
            return await _applescript_execute(arguments)
        elif name == "get_screen_resolution":
            return await _get_screen_resolution()
        elif name == "foreground_window":
            return await _foreground_window(arguments.get("app_name"))
        elif name == "dock_window_horizontal":
            return await _dock_window_horizontal(
                arguments.get("app_name"),
                arguments.get("left_percent"),
                arguments.get("right_percent")
            )
        elif name == "get_window_info":
            return await _get_window_info(arguments.get("app_name"))
        elif name == "get_system_info":
            return await _get_system_info()
        else:
            return [types.TextContent(type="text", text=f"Unknown macOS tool: {name}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error executing {name}: {str(e)}")]

async def _applescript_execute(arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Execute raw AppleScript code."""
        if not arguments or "code_snippet" not in arguments:
            return [types.TextContent(type="text", text="Error: Missing code_snippet argument")]

        timeout = arguments.get("timeout", 60)
        result = await execute_applescript(arguments["code_snippet"], timeout)
        return [types.TextContent(type="text", text=result)]

async def _get_screen_resolution() -> List[types.TextContent]:
        """Get screen resolution."""
        script = '''
        tell application "Finder"
            set screenBounds to bounds of window of desktop
            set screenWidth to item 3 of screenBounds
            set screenHeight to item 4 of screenBounds
            return "Resolution: " & screenWidth & "x" & screenHeight
        end tell
        '''
        result = await execute_applescript(script)
        return [types.TextContent(type="text", text=result)]

async def _foreground_window(app_name: str) -> List[types.TextContent]:
        """Bring application to foreground."""
        if not app_name:
            return [types.TextContent(type="text", text="Error: app_name is required")]

        script = f'''
        tell application "{app_name}"
            activate
        end tell
        '''
        await execute_applescript(script)
        return [types.TextContent(type="text", text=f"Successfully brought {app_name} to foreground")]

async def _dock_window_horizontal(app_name: str, left_percent: float, right_percent: float) -> List[types.TextContent]:
    """Dock window horizontally using percentage bounds."""
    if not app_name or left_percent is None or right_percent is None:
        return [types.TextContent(type="text", text="Error: app_name, left_percent, and right_percent are required")]

    if left_percent < 0 or left_percent > 100 or right_percent < 0 or right_percent > 100:
        return [types.TextContent(type="text", text="Error: percentages must be between 0 and 100")]

    if left_percent >= right_percent:
        return [types.TextContent(type="text", text="Error: left_percent must be less than right_percent")]

    # Get screen dimensions using existing function
    try:
        screen_result = await _get_screen_resolution()
        resolution_text = screen_result[0].text  # "Resolution: 1352x878"
        # Extract dimensions from "Resolution: WIDTHxHEIGHT"
        dimensions = resolution_text.split(": ")[1]  # "1352x878"
        screen_width, screen_height = map(int, dimensions.split('x'))
    except (ValueError, IndexError, AttributeError):
        return [types.TextContent(type="text", text=f"Error: Could not get screen dimensions")]

    # Calculate window bounds
    x_pos = int(screen_width * left_percent / 100)
    window_width = int(screen_width * (right_percent - left_percent) / 100)

    # First try to activate the application and get the process name
    activate_script = f'''
    tell application "{app_name}" to activate
    delay 0.5
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
        return frontApp
    end tell
    '''

    try:
        process_name = await execute_applescript(activate_script)
        process_name = process_name.strip()
    except Exception:
        process_name = app_name  # Fallback to provided name

    # Now dock the window using the actual process name
    script = f'''
    tell application "System Events"
        tell application process "{process_name}"
            set frontWindow to front window
            set position of frontWindow to {{{x_pos}, 0}}
            set size of frontWindow to {{{window_width}, {screen_height}}}
        end tell
    end tell
    '''

    await execute_applescript(script)
    return [types.TextContent(type="text", text=f"Window docked horizontally: {left_percent}%-{right_percent}% ({x_pos},{window_width}x{screen_height}) Process: {process_name}")]

async def _get_window_info(app_name: str = None) -> List[types.TextContent]:
        """Get window information."""
        if app_name:
            script = f'''
            tell application "System Events"
                tell process "{app_name}"
                    tell window 1
                        set windowPos to position
                        set windowSize to size
                        return "Position: " & item 1 of windowPos & "," & item 2 of windowPos & " Size: " & item 1 of windowSize & "x" & item 2 of windowSize
                    end tell
                end tell
            end tell
            '''
        else:
            script = '''
            tell application "System Events"
                set frontApp to name of first application process whose frontmost is true
                tell process frontApp
                    tell window 1
                        set windowPos to position
                        set windowSize to size
                        return "App: " & frontApp & " Position: " & item 1 of windowPos & "," & item 2 of windowPos & " Size: " & item 1 of windowSize & "x" & item 2 of windowSize
                    end tell
                end tell
            end tell
            '''

        result = await execute_applescript(script)
        return [types.TextContent(type="text", text=result)]

async def _get_system_info() -> List[types.TextContent]:
        """Get system information."""
        script = '''
        set computerName to computer name of (system info)
        set osVersion to system version of (system info)
        set totalMemory to (physical memory of (system info)) / 1024 / 1024
        return "Computer: " & computerName & " macOS: " & osVersion & " Memory: " & totalMemory & "MB"
        '''

        result = await execute_applescript(script)
        return [types.TextContent(type="text", text=result)]