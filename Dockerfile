# Use the FULL Python production layer instead of slim to auto-load system libraries
FROM python:3.11

WORKDIR /app

# Ensure pip handles dependency tree mapping smoothly
RUN pip install --no-cache-dir --upgrade pip

# Copy and install only your Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download standalone cloud-safe binaries for Playwright 
ENV PLAYWRIGHT_BROWSERS_PATH=/app/pw-browsers
RUN playwright install chromium

# Skip rigid Linux package validation checks on launch
ENV PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1

# Port over your main browser code file
COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
