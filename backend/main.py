from serpapi import GoogleSearch
import json
import re
import os

def search_prod(query):
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": "4e9f647b16dfb41ea8f762ea32fcdd25d104382d9e1fed6b7c9bcbc06e770570",  # Replace with your actual API key
        "tbm": "shop",
        "gl": "in"
    }
    search = GoogleSearch(params)
    result = search.get_dict()
    print("API response:", result)  # Check the full response from the API
    return result

def send_query(query):
    print("Received query:", query)
    results = search_prod(query)
    return results.get("shopping_results", [])

def filter_products(results, max_price):
    print("Filtering products below ₹", max_price)
    filtered = []

    for product in results:
        title = product.get("title")
        price = product.get("price")
        link = product.get("product_link")
        seller = product.get("source")

        # Parse numeric price
        if isinstance(price, str) and "₹" in price:
            match = re.search(r'[\d,.]+', price)
            price_val = float(match.group().replace(",", "")) if match else 0.0
        else:
            price_val = 0.0

        if price_val <= max_price:
            filtered.append({
                "title": title,
                "price": price,
                "link": link,
                "seller": seller
            })

    if not filtered:
        print("No products found within the price range.")
    return filtered

def save_results_to_json(data):
    os.makedirs('data', exist_ok=True)  # Ensure 'data' folder exists
    with open('data/api_results.json', 'w') as f:
        json.dump(data, f, indent=2)

def main():
    # Define the products and their max prices to search for
    query = {
        "iphone 15": 70000.00,  # Max price for iPhone 15
        "apple watch series 9": 40000.00  # Max price for Apple Watch Series 9
    }

    # Iterate through each product to search and filter results
    for product, max_price in query.items():
        results = send_query(product)  # Search for the product
        filtered_products = filter_products(results, max_price)  # Filter based on max price
        if filtered_products:  # If there are filtered products
            save_results_to_json(filtered_products)  # Save them to JSON file
            print(f"Results saved for {product}")
        else:
            print(f"No products found for {product}")

# Run the scraper
main()
