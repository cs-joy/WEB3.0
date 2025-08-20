FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV WEB3_PROVIDER_URL=http://host.docker.internal:8545
ENV IPFS_API_URL=/dns/ipfs/tcp/5001/http

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
