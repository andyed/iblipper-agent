#!/usr/bin/env bash
#
# iblipper.sh - Generate iBlipper URLs from the command line
#
# Usage:
#   iblipper.sh "Your Message"                    # Default (emphatic, dark)
#   iblipper.sh "Your Message" excited            # With emotion
#   iblipper.sh "Your Message" casual light       # With emotion + light mode
#   iblipper.sh --gif "Your Message" emphatic     # GIF export URL
#   iblipper.sh --pwa "Your Message"              # PWA protocol URL
#   iblipper.sh --aspect 1:1 "Your Message"       # Aspect ratio
#
# Outputs a ready-to-use URL, markdown link, or open command.

set -e

BASE_URL="https://andyed.github.io/iblipper2025/"

show_help() {
    cat << 'EOF'
iblipper.sh - Generate iBlipper kinetic typography URLs

USAGE:
    iblipper.sh [OPTIONS] "MESSAGE" [EMOTION] [MODE]

OPTIONS:
    --gif               Output GIF export URL (requires browser to download)
    --pwa               Output PWA protocol URL (web+iblipper:...)
    --markdown, -m      Output as markdown link with PLAY prefix
    --aspect VALUE      Aspect ratio (e.g., 16:9, 4:3, 1:1)
    --width VALUE       Output width in pixels
    --height VALUE      Output height in pixels
    --force-aspect      Force exact aspect; add padding if needed
    --help, -h          Show this help

ARGUMENTS:
    MESSAGE             Text to animate (required)
    EMOTION             Animation style (default: emphatic)
                        Options: neutral, hurry, idyllic, question, response_required,
                                 excited, playful, emphatic, casual, electric, wobbly
    MODE                dark (default) or light

EXAMPLES:
    iblipper.sh "Hello World"
    iblipper.sh "Breaking News" emphatic
    iblipper.sh "Good morning" casual light
    iblipper.sh -m "Click me!" excited
    iblipper.sh --gif "Export this" playful
    iblipper.sh --pwa "Open in App" excited
    iblipper.sh --aspect 1:1 "Square" emphatic

EOF
}

# Parse flags
GIF_MODE=false
PWA_MODE=false
MARKDOWN=false
FORCE_ASPECT=false
ASPECT=""
WIDTH=""
HEIGHT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --gif)
            GIF_MODE=true
            shift
            ;;
        --pwa)
            PWA_MODE=true
            shift
            ;;
        --markdown|-m)
            MARKDOWN=true
            shift
            ;;
        --aspect)
            ASPECT="${2:-}"
            if [[ -z "$ASPECT" ]]; then
                echo "Error: --aspect requires a value" >&2
                exit 1
            fi
            shift 2
            ;;
        --width)
            WIDTH="${2:-}"
            if [[ -z "$WIDTH" ]]; then
                echo "Error: --width requires a value" >&2
                exit 1
            fi
            shift 2
            ;;
        --height)
            HEIGHT="${2:-}"
            if [[ -z "$HEIGHT" ]]; then
                echo "Error: --height requires a value" >&2
                exit 1
            fi
            shift 2
            ;;
        --force-aspect)
            FORCE_ASPECT=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        -* )
            echo "Unknown option: $1" >&2
            exit 1
            ;;
        * )
            break
            ;;
    esac
done

# Get arguments
MESSAGE="${1:-}"
EMOTION="${2:-emphatic}"
MODE="${3:-dark}"

if [[ -z "$MESSAGE" ]]; then
    echo "Error: Message is required" >&2
    echo "Usage: iblipper.sh \"Your Message\" [emotion] [dark|light]" >&2
    exit 1
fi

# URL encode the message (spaces as +, special chars encoded)
# Uses sys.argv[1] to avoid shell quoting issues with the message content
encode_text() {
    local text="$1"
    python3 -c "import sys, urllib.parse; print(urllib.parse.quote_plus(sys.argv[1]))" "$text"
}

encode_param() {
    local text="$1"
    python3 -c "import sys, urllib.parse; print(urllib.parse.quote_plus(sys.argv[1]))" "$text"
}

ENCODED_TEXT=$(encode_text "$MESSAGE")

# Determine dark mode
DARK_BOOL="true"
[[ "$MODE" == "light" ]] && DARK_BOOL="false"

EXTRA_PARAMS=""
if [[ -n "$ASPECT" ]]; then
    ASPECT_ENC=$(encode_param "$ASPECT")
    EXTRA_PARAMS+="&aspect=${ASPECT_ENC}"
fi
if [[ -n "$WIDTH" ]]; then
    EXTRA_PARAMS+="&width=${WIDTH}"
fi
if [[ -n "$HEIGHT" ]]; then
    EXTRA_PARAMS+="&height=${HEIGHT}"
fi
if $FORCE_ASPECT; then
    EXTRA_PARAMS+="&forceAspect=true"
fi

# Build URL
if $GIF_MODE; then
    URL="${BASE_URL}?export=gif#text=${ENCODED_TEXT}&emotion=${EMOTION}&dark=${DARK_BOOL}${EXTRA_PARAMS}"
elif $PWA_MODE; then
    # PWA protocol: web+iblipper:MESSAGE
    # Note: PWA protocol currently only supports message text
    URL="web+iblipper:${ENCODED_TEXT}"
else
    # Standard Web URL
    URL="${BASE_URL}#text=${ENCODED_TEXT}&emotion=${EMOTION}&dark=${DARK_BOOL}&share=yes${EXTRA_PARAMS}"
fi

# Output
if $MARKDOWN; then
    if $PWA_MODE; then
       # For PWA in markdown, we can't really do a "link" that works everywhere, 
       # but we can try provided the client supports it.
       # Better to just output the command for the agent to run.
       echo "\`open \"${URL}\"\`"
    else
       echo "[PLAY ${MESSAGE}](${URL})"
    fi
elif $PWA_MODE; then
    # Output the command to run
    echo "open \"${URL}\""
else
    echo "$URL"
fi

