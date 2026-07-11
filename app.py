import os
import sys
import asyncio
import streamlit as st

# 1. FORCE THE PATH CORRECTION: Tell Playwright exactly where to look for the browser
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/app/pw-browsers"

# Streamlit App Configurations
st.set_page_config(page_title="Aevox Browser", layout="wide", page_icon="🌐")
st.title("🌐 Aevox Browser (Unblocked Engine)")

# Initialize session state tracking
if "url" not in st.session_state:
    st.session_state.url = "https://google.com"
if "screenshot" not in st.session_state:
    st.session_state.screenshot = None

# FIXED KEYWORD ARGUMENT: Changed unsafe_allowed_items to unsafe_allow_html
st.markdown("""
    <style>
    .stImage > img { border: 2px solid #333; border-radius: 8px; width: 100%; }
    </style>
""", unsafe_allow_html=True)

url_input = st.text_input("Enter URL Address:", value=st.session_state.url)

# Safe Auto-Installer Check to catch silent container lags
def ensure_browser_exists():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        st.error("Playwright package is still configuring. Please wait 10 seconds.")
        return False
    return True

async def capture_web_page(target_url):
    """Safely runs headless Chromium by bypassing root engine restrictions."""
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox", 
                    "--disable-setuid-sandbox", 
                    "--disable-dev-shm-usage", 
                    "--disable-gpu"
                ]
            )
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800}
            )
            page = await context.new_page()
            
            # Navigate with a generous time-limit buffer to prevent slow server timeouts
            await page.goto(target_url, timeout=20000, wait_until="load")
            screenshot_bytes = await page.screenshot(type="jpeg", quality=85)
            
            await context.close()
            await browser.close()
            return screenshot_bytes
            
        except Exception as e:
            st.warning(f"Aevox initialization lag detected. Attempting automatic bridge alignment...")
            os.system("python -m playwright install chromium")
            return None

# Execute safe pipeline
if ensure_browser_exists():
    if url_input != st.session_state.url or st.session_state.screenshot is None:
        if not url_input.startswith("http"):
            url_input = "https://" + url_input
        st.session_state.url = url_input
        
        with st.spinner("Aevox Engine routing to destination..."):
            img_data = asyncio.run(capture_web_page(st.session_state.url))
            if img_data:
                st.session_state.screenshot = img_data
                st.rerun()

# Display current captured state frame
if st.session_state.screenshot:
    st.image(st.session_state.screenshot, caption=f"Live View: {st.session_state.url}")
    
    if st.button("🔄 Interact / Refresh Page"):
        st.session_state.screenshot = None  # Force a clear re-fetch loop
        st.rerun()
