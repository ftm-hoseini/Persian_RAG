
FROM python:3.14-slim

# Set working directory
WORKDIR /app
ENV PYTHONPATH=/app

# Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements
COPY requirements.txt .

# Install dependencies using Runflare mirror
RUN pip install --no-cache-dir --upgrade pip \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install --no-cache-dir \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    -r requirements.txt

# Copy application source code
COPY src/ ./src/

# Create required directories
RUN mkdir -p /app/data/pdfs /app/chroma_db

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "src/app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.headless=true"]
