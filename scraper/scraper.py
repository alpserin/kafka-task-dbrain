from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from kafka import KafkaProducer
import json

# Set up the Selenium WebDriver
driver = webdriver.Chrome()

# URL to scrape
url = "https://scrapeme.live/shop/"

# Open the webpage
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Extract data from the table
products = []

# Locate the products
product_elements = driver.find_elements(By.CLASS_NAME, 'product')

# Debugging information
print(f"Found {len(product_elements)} products")

# Set up Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for index in range(len(product_elements)):
    product_elements = driver.find_elements(By.CLASS_NAME, 'product')
    product = product_elements[index]
    name = product.find_element(By.CLASS_NAME, 'woocommerce-loop-product__title').text.strip()
    price = product.find_element(By.CLASS_NAME, 'price').text.strip()
    
    # Click on the product link to go to the product details page
    product_link = product.find_element(By.TAG_NAME, 'a')
    product_link.click()
    
    # Wait for the product details page to load
    time.sleep(2)
    
    # Extract description and stock information
    try:
        description = driver.find_element(By.CSS_SELECTOR, '.woocommerce-product-details__short-description').text.strip()
    except:
        description = "No description available"
    
    try:
        stock = driver.find_element(By.CSS_SELECTOR, '.stock').text.strip()
    except:
        stock = "No stock information"

    product_data = {
        'name': name,
        'price': price,
        'description': description,
        'stock': stock
    }
    
    # Send data to Kafka topic
    print(f"Sending data to Kafka: {product_data}")
    producer.send('dbrain-topic', product_data)
    time.sleep(1)
    
    products.append(product_data)
    
    # Go back to the main shop page
    driver.back()
    
    # Wait for the main shop page to load
    time.sleep(2)

# Close the browser
driver.quit()

# Close the Kafka producer
producer.close()

# Save the data to a file
with open('products.json', 'w') as f:
    json.dump(products, f, indent=4)

# Display the data
print(products)
