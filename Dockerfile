# Pull clean, pre-compiled python stable image directly from Docker Hub 
FROM python:3.11-bookworm

WORKDIR /app

# Ensure local core library parameters are fully up to date
RUN pip install --no-cache-dir --upgrade pip

# Copy and install only your Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- THE FIX: Download the standalone chromium engine layout inside python environment ---
ENV PLAYWRIGHT_BROWSERS_PATH=/app/pw-browsers
RUN playwright install chromium
RUN playwright install-deps chromium
# -----------------------------------------------------------------------------------------

# Port over your main browser code file
COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
