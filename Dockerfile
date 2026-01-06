FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl git git-lfs && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

    
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV PYTHONPATH=/app/app

# Download assets DURING BUILD (cached layer)
ENV HF_MODELS_REPO=NenJa/astra-models
ENV HF_CHROMADB_REPO=NenJa/astra-chromadb

# Copy download script
COPY app/scripts/__init__.py app/scripts/
COPY app/scripts/download_assets.py app/scripts/
COPY app/src/settings.py app/src/



# Download assets during build with retries
RUN python3 -m app.scripts.download_assets || \
    (sleep 10 && python3 -m app.scripts.download_assets) || \
    (sleep 30 && python3 -m app.scripts.download_assets)

# NOW copy the rest of the app
COPY . .


EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Just start Streamlit - assets already present
ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]