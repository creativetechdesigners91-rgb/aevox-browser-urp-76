import os
import asyncio
import streamlit as st

# Tell Playwright exactly where the pre-downloaded browser lives
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/app/pw-browsers"

st.set_page_config(page_title="Aevox Browser", layout="wide", page_icon="🌐")
st.title("🌐 Aevox Browser")

if "url" not in st.session_state:
    st.session_state.url = "https://google.com"
if "screenshot" not in st.session_state:
    st.session_state.screenshot = None

st.markdown("""
    <style>
    .stImage > img { border: 2px solid #333; border-radius: 8px; width: 100%; }
    </style>
""", unsafe_allow_html=True)

url_input = st.text_input("Enter URL Address:", value=st.session_state.url)

async def capture_web_page(target_url):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        try:
            # Launch without a heavy sandbox layer to run fast on free cloud tiers
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
            )
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                viewport={"width": 1280, "height": 800}
            )
            page = await context.new_page()
            
            # Fast timeout prevents the spinning loop from freezing
            await page.goto(target_url, timeout=10000, wait_until="commit")
            screenshot_bytes = await page.screenshot(type="jpeg", quality=80)
            
            await context.close()
            await browser.close()
            return screenshot_bytes
        except Exception as e:
            st.error(f"Engine connection lag. Please try refreshing. Details: {str(e)}")
            return None

# Trigger capture loop
if url_input != st.session_state.url or st.session_state.screenshot is None:
    if not url_input.startswith("http"):
        url_input = "https://" + url_input
    st.session_state.url = url_input
    
    with st.spinner("Aevox Engine routing to destination..."):
        img_data = asyncio.run(capture_web_page(st.session_state.url))
        if img_data:
            st.session_state.screenshot = img_data
            st.rerun()

if st.session_state.screenshot:
    st.image(st.session_state.screenshot, caption=f"Live View: {st.session_state.url}")
    
    if st.button("🔄 Go / Refresh Page"):
        st.session_state.screenshot = None
        st.rerun()
