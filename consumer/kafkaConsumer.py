from kafka import KafkaConsumer
import json

# Set up Kafka consumer
consumer = KafkaConsumer(
    'dbrain-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')) if v else None
)

products = []

for message in consumer:
    try:
        # Raw message
        raw_value = message.value
        print(f"Raw message: {raw_value}")

        # Check if the message is empty or None
        if raw_value is None:
            print("Skipped an empty message.")
            continue

        # Deserialize message
        product_data = message.value

        # Validate the structure of the JSON
        if not isinstance(product_data, dict) or 'name' not in product_data or 'price' not in product_data:
            print(f"Invalid message format: {product_data}")
            continue

        products.append(product_data)

        # Save to file after every message
        with open('products_from_kafka.json', 'w') as f:
            json.dump(products, f, indent=4)
        print(f"Saved product: {product_data}")
        
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Close the Kafka consumer
consumer.close()
