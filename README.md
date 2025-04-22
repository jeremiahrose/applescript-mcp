# AppleScript MCP Server (Dual access: python and node.js)

## Overview

A Model Context Protocol (MCP) server that lets you run AppleScript code to interact with Mac. This MCP is intentionally designed to be simple, straightforward, intuitive, and require minimal setup.

I can't believe how simple and powerful it is. The core code is <100 line of code.

## Features

* Run AppleScript to access Mac applications and data
* Interact with Notes, Calendar, Contacts, Messages, and more
* Search for files using Spotlight or Finder
* Read/write file contents and execute shell commands

## Example Prompts

```
Create a reminder for me to call John tomorrow at 10am
```

```
Add a new meeting to my calendar for Friday from 2-3pm titled "Team Review"
```

```
Create a new note titled "Meeting Minutes" with today's date
```

```
Show me all files in my Downloads folder from the past week
```

```
What's my current battery percentage?
```

```
Show me the most recent unread emails in my inbox
```

```
List all the currently running applications on my Mac
```

```
Play my "Focus" playlist in Apple Music
```

```
Take a screenshot of my entire screen and save it to my Desktop
```

```
Find John Smith in my contacts and show me his phone number
```

```
Create a folder on my Desktop named "Project Files"
```

```
Open Safari and navigate to apple.com
```

```
Tell me how much free space I have on my main drive
```

```
List all my upcoming calendar events for this week
```

## Usage with Claude Desktop

### Node.js
```json
{
  "mcpServers": {
    "applescript_execute": {
      "command": "npx",
      "args": [
        "/path/to/repo/server.js"
      ]
    }
  }
}
```

### Python
Install uv
```
brew install uv
```
Run the server
```
{
  "mcpServers": {
    "applescript_execute": {
      "command": "uv",
      "args": [
        "run",
        "/path/to/repo/server.js"
      ]
    }
  }
}
```