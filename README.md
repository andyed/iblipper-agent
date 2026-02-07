# iBlipper

**Kinetic Typography for AI Agents.**

iBlipper allows AI agents to communicate with visual flair using animated text. It supports:
- **Web Links**: Shareable URLs that play animations.
- **PWA Protocol**: Direct deep-linking to the iBlipper PWA.
- **MCP Server**: Universal skill for Claude Desktop and other MCP-compliant agents.

## Installation

### Via `uv` (Recommended)

```bash
uv tool install iblipper
```

### From Source

```bash
git clone https://github.com/andyed/iblipper.git
cd iblipper
pip install .
```

## Usage

### CLI

```bash
# Generate a link
iblipper.sh "Hello World"

# PWA Protocol
iblipper.sh --pwa "Hello World"
```

*Note: The script is located at `src/iblipper/scripts/iblipper.sh`.*

### MCP Server (Claude Desktop)

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "iblipper": {
      "command": "uv",
      "args": ["tool", "run", "iblipper-server"]
    }
  }
}
```

### Local GIF Generation (Owning the File)

You can generate GIFs locally using the included renderer (requires Playwright).

**Via Python:**
```python
import asyncio
from iblipper.renderer import render_gif

asyncio.run(render_gif(
    "https://andyed.github.io/iblipper2025/?export=gif#text=Hello",
    "output.gif"
))
```

**Via MCP Tool:**
Use `render_gif_file(message="Hello", output_path="hello.gif")`.
