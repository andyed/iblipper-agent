
import urllib.parse

BASE_URL = "https://andyed.github.io/iblipper2025/"

def generate_iblipper_url(
    message: str,
    emotion: str = "emphatic",
    dark: bool = True,
    pwa: bool = False,
    gif: bool = False,
    aspect: str | None = None,
    width: int | None = None,
    height: int | None = None,
    force_aspect: bool = False,
) -> str:
    """
    Generate an iBlipper URL or PWA protocol string.
    """
    encoded_text = urllib.parse.quote_plus(message)
    
    if pwa:
        return f"web+iblipper:{encoded_text}"
        
    params = []
    
    # Core params
    if gif:
        base = f"{BASE_URL}?export=gif"
        # GIF export doesn't use hash params usually in the same way, but let's follow the script's pattern
        # Script: URL="${BASE_URL}?export=gif#text=${ENCODED_TEXT}&emotion=${EMOTION}&dark=${DARK_BOOL}${EXTRA_PARAMS}"
        # The script puts the rest in hash.
        fragment_params = [
            f"text={encoded_text}",
            f"emotion={emotion}",
            f"dark={'true' if dark else 'false'}"
        ]
    else:
        base = BASE_URL
        fragment_params = [
            f"text={encoded_text}",
            f"emotion={emotion}",
            f"dark={'true' if dark else 'false'}",
            "share=yes"
        ]

    # Extra params
    if aspect:
        fragment_params.append(f"aspect={urllib.parse.quote_plus(aspect)}")
    if width:
        fragment_params.append(f"width={width}")
    if height:
        fragment_params.append(f"height={height}")
    if force_aspect:
        fragment_params.append(f"forceAspect=true")
        
    return f"{base}#{'&'.join(fragment_params)}"
