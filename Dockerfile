FROM python:3.11-slim

WORKDIR /

# Install curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# RUN git clone https://github.com/mujeeb-gh/rag-chatbot-final.git .

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

WORKDIR /app

# Create entrypoint script that downloads assets before starting Streamlit
RUN echo '#!/bin/bash\n\
python3 /app/scripts/download_assets.py\n\
exec streamlit run main.py --server.port=8501 --server.address=0.0.0.0\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]