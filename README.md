# macOS Control MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

The goal is to create a comprehensive Model Context Protocol (MCP) server for full macOS system control through AppleScript. This server provides both raw AppleScript execution capabilities and structured tools for common macOS operations like window management, system information, and application control.

Originally forked from [peakmojo/applescript-mcp](https://github.com/peakmojo/applescript-mcp), but the intention is to expanded towards a full-fledged macOS automation platform with dedicated modules for commonly used applications and system functions.

## Goals

- **Full macOS System Control**: Comprehensive automation of macOS through AppleScript
- **Modular Architecture**: Dedicated modules for specific applications
- **Structured Tools**: High-level tools for common operations alongside raw AppleScript access

## Current features

* **Raw AppleScript Execution**: Run any AppleScript code for maximum flexibility
* **Structured Window Management**: Dock windows horizontally using percentage bounds
* **System Information**: Get screen resolution, system specs, and window details
* **Application Control**: Foreground applications and manage processes
* **Dynamic Screen Detection**: Automatically fetch screen dimensions for precise positioning
* **Modular Design**: Easy to extend with new application-specific modules

## Available Tools

### Core System Tools
- **`applescript_execute`**: Execute raw AppleScript code for maximum flexibility
- **`get_screen_resolution`**: Get current screen resolution and display information
- **`get_system_info`**: Get macOS version, computer name, and memory information
- **`get_window_info`**: Get position and size information for windows

### Window Management
- **`dock_window_horizontal`**: Position windows using percentage bounds
  - Example: `dock_window_horizontal("iTerm", 0, 50)` - dock iTerm to left half
  - Example: `dock_window_horizontal("Safari", 50, 100)` - dock Safari to right half
  - Example: `dock_window_horizontal("Code", 25, 75)` - dock VSCode to middle 50%

### Application Control
- **`foreground_window`**: Bring a specific application to the foreground

## Example Usage

### Window Management
```
Dock iTerm to the left half of my screen
```

```
Position Safari on the right third of my screen
```

```
Move VSCode to take up the middle 60% of my screen
```

### System Information
```
What's my current screen resolution?
```

```
Show me my system information
```

```
Get the position and size of the frontmost window
```

### Raw AppleScript
```
Create a new note in Apple Notes with today's date
```

```
Get my current battery percentage
```

```
List all running applications
```

## Installation & Usage

### Prerequisites
- macOS system
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup
1. Install uv:
   ```bash
   brew install uv
   ```

2. Clone this repository:
   ```bash
   git clone <repository-url>
   cd applescript-mcp
   ```

3. The server will automatically install dependencies when run with uv.

### Claude Desktop Configuration

Add this to your Claude Desktop `mcp.json` configuration:

```json
{
  "mcpServers": {
    "macos-control": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/your/applescript-mcp",
        "python",
        "-m",
        "src.applescript_mcp"
      ],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

Replace `/path/to/your/applescript-mcp` with the actual path to your cloned repository.

### Development

The server uses a modular architecture located in `src/applescript_mcp/`:

- `tools/macos.py` - Core macOS system tools
- `utils/applescript.py` - AppleScript execution utilities
- `server.py` - Main MCP server

To add new application-specific modules, create new files in the `tools/` directory following the same pattern as `macos.py`.
