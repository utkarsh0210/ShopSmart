from flask import Flask, jsonify, request

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "Welcome to ShopSmart!"

if __name__ == "__main__":
    app.run(debug=True)
