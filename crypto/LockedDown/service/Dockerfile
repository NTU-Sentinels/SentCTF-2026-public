FROM python:3.12-slim

WORKDIR /challenge

RUN apt-get update && \
    apt-get install -y socat && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod +x start.sh

EXPOSE 31337

CMD ["./start.sh"]
