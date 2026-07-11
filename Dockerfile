# Match your local system running Python 3.14
FROM python:3.14-slim

WORKDIR /app

# Copy dependency records
COPY requirements.txt .

# Install packages via pip
RUN pip install --no-cache-dir -r requirements.txt

# Download and configure standalone browser binaries for Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

# Port over the browser code file
COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
