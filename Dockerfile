# Use an image fully pre-configured for web apps
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install only essential font libraries so text can render on the canvas
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download isolated cloud-safe binaries for Playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/app/pw-browsers
RUN playwright install chromium

COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
