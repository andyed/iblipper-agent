
import asyncio
from playwright.async_api import async_playwright
import os

async def render_gif(url: str, output_path: str, width: int = 480, height: int = 480):
    """
    Renders an iBlipper URL to a GIF file using Playwright.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Grant permissions for clipboard if needed, though likely not for GIF export
        context = await browser.new_context(
            viewport={'width': width, 'height': height},
            device_scale_factor=2
        )
        page = await context.new_page()

        print(f"Navigating to {url}...")
        try:
            # Wait for network idle to ensure app is loaded
            await page.goto(url, wait_until='networkidle', timeout=60000)
            print("Page loaded.")
        except Exception as e:
            print(f"Navigation error (might be okay if app loaded): {e}")

        # Inject script to force start recording if it didn't auto-start
        # We also need to mock the 'user interaction' if needed for audio context (though we don't need audio for GIF)
        
        print("Injecting recording trigger...")
        
        # Let's assume we need to click the "Share" or "Export" button if not auto.
        # For now, let's try to detect if a blob is generated or download triggered.
        
        # Scenario: User wants a GIF file.
        # We can use the 'screencast' feature or just let the app generate it.
        # If the app generates a Blob URL, we can intercept the download.
        
        # Setup download listener
        # Monitor console logs
        page.on("console", lambda msg: print(f"PAGE LOG: {msg.text}"))

        async with page.expect_download(timeout=180000) as download_info:
             # If the URL has 'share=yes', does it auto-download? Probably not.
             # We might need to click a button.
             # Let's assume there is an export button accessible.
             # Or we can inject script to trigger the export logic.
             
             # INJECT TRIGGER:
             # useRSVPStore.getState().startGifRecording()
             
             print("Waiting for store to be ready...")
             # Wait for store
             await page.wait_for_function("() => window.useRSVPStore !== undefined")
             print("Store ready. Starting recording...")
             
             # Use higher multiplier (skip more frames) to speed up encoding for long texts
             # density=0 means all words at once? No, default density.
             # The URL has density=0. Wait, density=0 might mean "all at once"?
             # Let's check store.ts.
             
             await page.evaluate("() => { window.useRSVPStore.getState().setGifFrameMultiplier(15); window.useRSVPStore.getState().startGifRecording(); }")
             
             # The app should now record and eventually trigger a download.
             # We need to wait for the recording to finish.
             pass

        download = await download_info.value
        await download.save_as(output_path)
        print(f"Saved GIF to {output_path}")

        await browser.close()

if __name__ == "__main__":
    # Test with user provided URL
    target_url = "https://andyed.github.io/iblipper2025/#text=The+only+thing+necessary+for+the+triumph+of+evil+is+for+good+men+to+do+nothing.&wpm=200&density=0&fill=true&theme=0&dark=false&emotion=emphatic"
    asyncio.run(render_gif(target_url, "src/iblipper/resources/example.gif"))
