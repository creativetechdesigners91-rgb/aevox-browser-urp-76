# Use Microsoft's official pre-built production container for Playwright
FROM ://microsoft.com

WORKDIR /app

# Ensure pip is up to date inside the container
RUN pip install --no-cache-dir --upgrade pip

# Copy and install only your Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Port over your main browser code file (playwright binaries are already inside!)
COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
