#!/bin/sh
sleep 10  # Wait for 10 seconds to ensure Kafka is up
python kafkaConsumer.py
