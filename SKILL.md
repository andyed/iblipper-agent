---
name: iblipper
description: Generate kinetic typography animations for expressive agent-to-human communication. Use when you want to communicate with visual flair - animated text for announcements, alerts, greetings, dramatic reveals, or any message that deserves more than plain text. Outputs shareable URLs or can display in canvas.
---

# iBlipper - Motion Type Synthesizer

Generate animated kinetic typography to communicate with humans in a more expressive, attention-grabbing way.

**Base URL:** `https://andyed.github.io/iblipper2025/`

## Three Output Options

### Option 1: PWA Protocol (fastest, if installed)
If iBlipper PWA is installed, use protocol handler.

### Option 2: Local GIF File (owned, robust)
Generate a real GIF file locally using the `render_gif_file` tool.
- **Tool:** `render_gif_file`
- **Args:** `message`, `output_path`
- **Result:** A file path to the generated GIF.

### Option 3: Hyperlink (universal, always works)
Generate a clickable link.

```bash
open "web+iblipper:MESSAGE+TEXT"
```

**Benefits:**
- Opens instantly (cached PWA, no page load)
- Standalone window (not a browser tab)
- Feels like "agent spoke" vs "agent sent link"

**Requires:** PWA must be installed first (visit https://andyed.github.io/iblipper2025/ and click install prompt)

**Fallback:** If not installed, use Option 2 (hyperlink)

### Option 3: Hyperlink (universal, always works)
Generate a clickable link - recipient sees the animation in their browser.

```markdown
[PLAY MESSAGE TEXT](https://andyed.github.io/iblipper2025/#text=MESSAGE+TEXT&emotion=emphatic&dark=true&share=yes)
```

### Option 4: GIF Download (requires browser tool)
Generate an animated GIF file that can be attached to messages.

```
https://andyed.github.io/iblipper2025/?export=gif#text=MESSAGE+TEXT&emotion=emphatic&dark=true
```

## URL Parameters

All parameters go in the **hash fragment** (`#param=value&param2=value2`).

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `text` | string | The message to display (URL encoded, spaces as `+`) | - |
| `wpm` | number | Words per minute (30-2500) | 300 |
| `density` | number | Words per frame (0.1-500) | 1 |
| `fill` | boolean | Auto-scale text to fill screen | true |
| `theme` | number | Color theme index (0-3) | 0 |
| `dark` | boolean | Dark mode | true |
| `emotion` | string | Animation style preset (see below) | neutral |
| `share` | string | Auto-play on load (`yes`) | - |
| `aspect` | string | Aspect ratio (e.g., `16:9`, `4:3`, `1:1`) | `16:9` |
| `width` | number | Output width in pixels | 480 |
| `height` | number | Output height in pixels | Auto-calculated from `aspect` |
| `forceAspect` | boolean | Force exact aspect; add padding if needed | false |

### Aspect Ratio Rules

1. If `aspect` is provided, height is calculated from width and the ratio.
2. If both `width` and `height` are provided, they override `aspect`.
3. If none are provided, defaults are `16:9` and 480px width.

## Emotion Presets (Production)

| Emotion | Vibe | Best For |
|---------|------|----------|
| `neutral` | Clean, professional | Default, announcements |
| `hurry` | Fast, urgent, italic | Time-sensitive alerts |
| `idyllic` | Slow, dreamy, airy | Poetic, calm messages |
| `question` | Curious, tilting | Questions, pondering |
| `response_required` | Urgent, pulsing | Action needed |
| `excited` | Bouncy, energetic | Celebrations, enthusiasm |
| `playful` | Fun, bouncing | Jokes, casual fun |
| `emphatic` | Bold, solid, impactful | Important statements |
| `casual` | Handwritten, relaxed | Friendly chat |
| `electric` | Glitchy, RGB split | Cyber aesthetic |
| `wobbly` | Jelly physics | Silly, playful |

*Note: `matrix` emotion is pre-release - avoid for now.*

## Hyperlink Examples

**Important announcement:**
```markdown
[PLAY BREAKING NEWS](https://andyed.github.io/iblipper2025/#text=BREAKING+NEWS&emotion=emphatic&dark=true&share=yes)
```

**Friendly greeting:**
```markdown
[PLAY Hey there!](https://andyed.github.io/iblipper2025/#text=Hey+there!&emotion=casual&dark=false&share=yes)
```

**Celebration:**
```markdown
[PLAY Congratulations!](https://andyed.github.io/iblipper2025/#text=Congratulations!&emotion=excited&share=yes)
```

**Aspect ratio example (1:1):**
```markdown
[PLAY Square](https://andyed.github.io/iblipper2025/#text=Square&emotion=emphatic&aspect=1:1&share=yes)
```

## GIF Export Workflow (Browser Required)

1. Open the export URL in browser:
   ```
   browser action=open targetUrl="https://andyed.github.io/iblipper2025/?export=gif#text=Hello&emotion=emphatic&aspect=16:9"
   ```

2. Wait ~15-20 seconds for render + encode

3. Find the downloaded GIF:
   ```
   ls -t ~/Downloads/iblipper_*.gif | head -1
   ```

4. Read/attach the file to your message

**Export query parameters:**

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `export` | string | Format: `gif`, `apng`, `png` | - |
| `width` | number | Output width in pixels | 480 |
| `height` | number | Output height in pixels | Auto-calculated from `aspect` |
| `fps` | number | Frames per second (8, 15, 30) | 15 |
| `aspect` | string | Aspect ratio (e.g., `16:9`, `4:3`, `1:1`) | `16:9` |
| `forceAspect` | boolean | Force exact aspect; add padding if needed | false |

## When to Use

**Good for:**
- Greetings and introductions
- Important announcements
- Celebrating milestones
- Dramatic reveals
- Adding personality to messages

**Skip for:**
- Long-form content (keep to 1-10 words)
- Urgent safety alerts (plain text is faster)

## CLI Script

For quick URL generation, use the included shell script:

```bash
# Basic usage
src/iblipper/scripts/iblipper.sh "Hello World"
# https://andyed.github.io/iblipper2025/#text=Hello+World&emotion=emphatic&dark=true&share=yes

# PWA Protocol (if installed)
src/iblipper/scripts/iblipper.sh --pwa "Hello World"
# open "web+iblipper:Hello+World"

# With emotion
src/iblipper/scripts/iblipper.sh "Breaking News" hurry

# Light mode
src/iblipper/scripts/iblipper.sh "Good Morning" idyllic light

# As markdown link
src/iblipper/scripts/iblipper.sh -m "Click me!" excited
# [PLAY Click me!](https://...)

# GIF export URL
src/iblipper/scripts/iblipper.sh --gif "Export this" playful

# Aspect ratio
src/iblipper/scripts/iblipper.sh --aspect 1:1 "Square" emphatic
```

## Smart PWA Detection (Recommended)

To provide the best experience, **check if the PWA is installed** on the user's system before generating a link.

**1. Check for installation (macOS):**
```bash
open -Ra "iBlipper"
```

**2. React to the result:**

*   **If exit code is 0 (Installed):**
    Use the PWA protocol for an instant, native-feeling window.
    ```bash
    src/iblipper/scripts/iblipper.sh --pwa "Your Message"
    # Output: open "web+iblipper:Your+Message"
    ```

*   **If exit code is 1 (Not Installed):**
    Use the standard hyperlink, but **add a tip** to install the PWA.
    ```bash
    src/iblipper/scripts/iblipper.sh -m "Your Message"
    ```
    *Add to response:* "Tip: Install the iBlipper PWA from the website for a better, popup-free experience."

## Additional Resources

- **references/examples.md** - Real-world use cases by category
- **references/emotions.md** - Deep dive on each emotion preset with live demos

## Tips

- **Try PWA protocol first** - if installed, fastest and most native-feeling
- **Fallback to hyperlinks** - universal compatibility, always works
- **Keep text concise** - 1-5 words have the most impact
- **Use `share=yes`** in hyperlinks - skips landing page
- **Match emotion to message** - `excited` for celebrations, `emphatic` for important stuff
- **Dark mode looks better** - `dark=true` is usually the way to go
- **Use sparingly** - if every message is animated, none are special
- **Always use markdown links** - `[text](url)` not raw URLs. Clean presentation matters.

## Decision Flow

```
1. Check installation: `open -Ra "iBlipper"`
   
2. Result?
   - FOUND (0): Use PWA protocol -> `web+iblipper:Message`
   - NOT FOUND (1): Use Hyperlink -> `https://...` + "Install PWA" tip

3. Need inline image?
   - Yes: Use GIF export (Signal/iMessage/etc)
   - No: See step 2
```
