FROM ubuntu:26.04

RUN apt-get update && \
    apt-get install -y socat && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /challenge

COPY luckyDraw3 .
COPY flag.txt .
COPY start.sh .

RUN chmod +x luckyDraw3 start.sh

EXPOSE 6767

CMD ["./start.sh"]
