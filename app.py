import streamlit as st
import asyncio
from playwright.async_api import async_playwright

st.set_page_config(page_title="Aevox Browser", layout="wide", page_icon="🌐")
st.title("🌐 Aevox Browser (Unblocked Engine)")

if "url" not in st.session_state:
    st.session_state.url = "https://google.com"
if "screenshot" not in st.session_state:
    st.session_state.screenshot = None

st.markdown("""
    <style>
    .stImage > img { border: 2px solid #333; border-radius: 8px; width: 100%; }
    </style>
""", unsafe_allowed_items=True)

url_input = st.text_input("Enter URL Address:", value=st.session_state.url)

async def capture_web_page(target_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()
        try:
            await page.goto(target_url, timeout=15000, wait_until="load")
            screenshot_bytes = await page.screenshot(type="jpeg", quality=80)
            return screenshot_bytes
        except Exception as e:
            st.error(f"Failed to load page: {str(e)}")
            return None
        finally:
            await context.close()
            await browser.close()

if url_input != st.session_state.url or st.session_state.screenshot is None:
    if not url_input.startswith("http"):
        url_input = "https://" + url_input
    st.session_state.url = url_input
    
    with st.spinner("Aevox Engine routing to destination..."):
        img_data = asyncio.run(capture_web_page(st.session_state.url))
        if img_data:
            st.session_state.screenshot = img_data

if st.session_state.screenshot:
    st.image(st.session_state.screenshot, caption=f"Live View: {st.session_state.url}")
    
    if st.button("🔄 Interact / Refresh Page"):
        st.rerun()
