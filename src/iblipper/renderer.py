
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

async def render_gif(url: str, output_path: str, timeout: int = 30000) -> str:
    """
    Render an iBlipper URL to a GIF file using a headless browser.
    
    Args:
        url: The iBlipper URL (must have export=gif or similar that triggers download/render).
             For iBlipper, we usually construct it specifically for export.
        output_path: Path to save the GIF to.
        timeout: Timeout in milliseconds.
        
    Returns:
        The absolute path to the saved GIF.
    """
    output_path = Path(output_path).resolve()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()
        
        # iBlipper specific: The render starts immediately, and download triggers automatically 
        # when done. We need to catch the download event.
        
        # If the URL doesn't have export=gif, we might need to inject it or handle it.
        # Assuming the caller provides the correct export URL.
        
        async with page.expect_download(timeout=timeout) as download_info:
            await page.goto(url)
            # We might need to wait for some condition if the download doesn't start immediately
            # iBlipper usually shows a "Rendering..." screen then downloads.
            
        download = await download_info.value
        await download.save_as(output_path)
        
        await browser.close()
        
    return str(output_path)
