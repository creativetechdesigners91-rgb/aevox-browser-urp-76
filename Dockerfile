# Use a clean, stable base image
FROM python:3.11-slim-bookworm

WORKDIR /app

# --- THE FIX: Install core Linux system GUI packages to provide all 26 missing libraries ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgtk-3-0 \
    libasound2 \
    libnss3 \
    libxss1 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*
# -----------------------------------------------------------------------------------------

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download standalone cloud-safe binaries for Playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/app/pw-browsers
RUN playwright install chromium

COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
