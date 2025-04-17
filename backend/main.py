from serpapi import GoogleSearch
import json
import re

def search_prod(query):
    params = {
      "engine": "google_shopping",
      "q": query,
      "api_key": "4e9f647b16dfb41ea8f762ea32fcdd25d104382d9e1fed6b7c9bcbc06e770570",
      "tbm": "shop",
      "gl":"in"
    }
    search = GoogleSearch(params)
    rslt = search.get_dict()
    return rslt


def send_query(query):
    print("received query for "+query)
    results = search_prod(query)
    if "shopping_results" in results:
        return results["shopping_results"]
    else:
        print(f"No results found for query: {query}")
        return []  # Return an empty list if no results found


# Extract and filter the title, price, product link, and seller name for each product within the price range
def display_result(results,max_price):
    print(f"max_price received as : {max_price}")
    filtered_products = []
    for product in results:
        title = product.get("title")
        price = product.get("price")
        link = product.get("product_link")
        seller = product.get("source")

        # Extract numeric value from price string
        if isinstance(price, str) and price:  # Check if price is a valid string
            price_match = re.search(r'[\d,.]+', price) if '₹' in price else None
            price_value = float(price_match.group().replace(',', '').replace('/mo', '').strip()) if price_match else 0.0
        else:
            price_value = 0.0  # Default value if price is not valid

        if price_value <= max_price:
            filtered_products.append({
                "title": title,
                "price": price,
                "link": link,
                "seller": seller
            })
    return filtered_products

def save_results_to_json(filtered_products):
    # Save the filtered results to a JSON file, overwriting existing content
    with open('api_results.json', 'w') as json_file:
        json.dump(filtered_products, json_file, indent=4)


def main():
    query = {"iphone 15":70000.00 , "apple watch series 9":40000.00}
    for p in query:
        results = send_query(p)
        filtered_products = display_result(results,query[p])
        print(filtered_products[0])
        save_results_to_json(filtered_products)

main()
