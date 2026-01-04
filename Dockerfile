FROM python:3.11-slim

WORKDIR /app

# Install only curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies FIRST (this layer only rebuilds when requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code LAST (changes here won't invalidate pip install)
COPY . .

ENV PYTHONPATH=/app/app

# Create entrypoint script
RUN echo '#!/bin/bash\n\
python3 -m app.scripts.download_assets\n\
exec streamlit run app/main.py --server.port=8501 --server.address=0.0.0.0\n\
' > /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["/entrypoint.sh"]