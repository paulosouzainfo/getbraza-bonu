FROM python:3.11-slim-bullseye

EXPOSE 8000

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# sonarcloud-scan ignore
COPY . .

RUN pip install --upgrade pip && \
    pip install crypto_keys_values_store-0.0.5.tar.gz && \
    pip install --no-cache-dir -r requirements/requirements.txt

ENTRYPOINT [ "streamlit", "run", "main.py", "--server.port=8000", "--server.address=0.0.0.0" ]
# streamlit run main.py --server.port=8000 --server.address=0.0.0.0
