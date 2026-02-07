from mcp.server.fastmcp import FastMCP
from iblipper.logic import generate_iblipper_url
from iblipper.renderer import render_gif
import os

mcp = FastMCP("iblipper")

@mcp.tool()
def generate_url(
    message: str,
    emotion: str = "emphatic",
    dark: bool = True,
    pwa: bool = False,
    gif: bool = False, 
    aspect: str | None = None,
) -> str:
    """
    Generate a kinetic typography animation URL for a message.
    
    Args:
        message: The text to animate. Keep it short (1-5 words) for maximum impact.
        emotion: The animation style. Options: 
                 - 'neutral': Clean, professional
                 - 'emphatic': Bold, important (default)
                 - 'hurry': Urgent, italic
                 - 'excited': Bouncy, incorrect
                 - 'playful': Fun, casual
                 - 'idyllic': Slow, peaceful
                 - 'question': Curious
        dark: Use dark mode (True) or light mode (False). Dark mode is recommended.
        pwa: If True, returns a 'web+iblipper:...' protocol string to open the PWA directly.
             Only use this if you know the user has the iBlipper PWA installed.
        gif: If True, returns a URL to generate/download a GIF of the animation.
        aspect: Aspect ratio (e.g., "16:9", "1:1").
    """
    return generate_iblipper_url(
        message=message,
        emotion=emotion,
        dark=dark,
        pwa=pwa,
        gif=gif,
        aspect=aspect
    )

@mcp.tool()
async def render_gif_file(
    message: str,
    output_path: str,
    emotion: str = "emphatic",
    dark: bool = True,
    aspect: str | None = None,
) -> str:
    """
    Render a GIF animation locally and save it to a file.
    
    Args:
        message: The text to animate.
        output_path: The file path to save the GIF to (e.g., "/tmp/animation.gif").
        emotion: Animation style.
        dark: Dark mode.
        aspect: Aspect ratio.
    """
    # 1. Generate the Export URL
    url = generate_iblipper_url(
        message=message,
        emotion=emotion,
        dark=dark,
        gif=True, # Important to trigger export mode
        aspect=aspect
    )
    
    # 2. Render it
    try:
        saved_path = await render_gif(url, output_path)
        return f"Successfully saved GIF to {saved_path}"
    except Exception as e:
        return f"Failed to render GIF: {str(e)}"


if __name__ == "__main__":
    mcp.run()
