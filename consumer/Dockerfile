FROM python:3.11-slim

WORKDIR /app

COPY kafkaConsumer.py /app
COPY requirements.txt /app
COPY start-consumer.sh /app

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x start-consumer.sh

CMD ["./start-consumer.sh"]
