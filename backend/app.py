from flask import Flask, jsonify, request
from main import send_query, filter_products, save_results_to_json
import os


app = Flask(__name__)
os.makedirs("data",exist_ok=True)

# Home route
@app.route('/')
def index():
    return "Welcome to ShopSmart!"

@app.route('/products', methods=['POST'])
def get_products():
    data = request.get_json()
    search_query = data.get("searchQuery")
    min_price = int(data.get("minPrice",0))
    max_price = int(data.get("maxPrice",10000000))

    if not search_query:
        return jsonify({"error": "Missing required parameter 'searchQuery'"}), 400
    
    results = send_query(search_query)
    filtered = filter_products(results, max_price)
    save_results_to_json(filtered)

    return jsonify({"status": "success", "count": len(filtered)})

if __name__ == "__main__":
    app.run(debug=True)
