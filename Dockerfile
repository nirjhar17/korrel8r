FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY openshift_ai_analyzer.py .
COPY openshift_alerting.py .
COPY simple_test.py .

# Create non-root user
RUN useradd -m -u 1000820000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose ports
EXPOSE 8080 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command
CMD ["python", "-m", "streamlit", "run", "simple_test.py", "--server.port=8501", "--server.address=0.0.0.0"]









