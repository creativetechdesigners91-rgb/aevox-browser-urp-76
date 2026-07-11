# Down grade the cloud container engine to a stable production version
FROM python:3.11-slim

WORKDIR /app

# Upgrade pip to ensure secure dependency mapping
RUN pip install --no-cache-dir --upgrade pip

# Copy dependency records
COPY requirements.txt .

# Install packages via pip cleanly
RUN pip install --no-cache-dir -r requirements.txt

# Download and configure standalone browser binaries for Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

# Port over the browser code file
COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
