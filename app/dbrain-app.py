from flask import Flask, jsonify
import json

app = Flask(__name__)

# Load data from file
with open('products_from_kafka.json', 'r') as f:
    products = json.load(f)

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    if 0 <= product_id < len(products):
        return jsonify(products[product_id])
    else:
        return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
