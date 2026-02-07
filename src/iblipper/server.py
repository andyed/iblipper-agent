from mcp.server.fastmcp import FastMCP
from iblipper.logic import generate_iblipper_url
from iblipper.renderer import render_gif
import os
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
    output_filename: str,
    emotion: str = "emphatic",
    dark: bool = True,
    width: int = 480,
    height: int = 480
) -> str:
    """
    Renders an iBlipper animation to a local GIF file.
    Args:
        message: The text content
        output_filename: The local filename to save (e.g., 'animation.gif')
        emotion: The emotional tone
        dark: Whether to use dark mode
        width: Output width
        height: Output height
    Returns:
        The text indicating success.
    """
    url = generate_iblipper_url(message, emotion=emotion, dark=dark, pwa=False, aspect="1:1") # Square for GIF
    # Ensure export=gif is not needed in URL if we drive it via renderer script, 
    # but let's assume valid URL
    
    # Resolve absolute path for output
    full_path = os.path.abspath(output_filename)
    
    await render_gif(url, full_path, width, height)
    return f"GIF saved to {full_path}"

if __name__ == "__main__":
    mcp.run()
