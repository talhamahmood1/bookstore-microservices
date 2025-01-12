from flask import Flask, render_template
import requests

app = Flask(__name__, static_folder='static')


CATALOG_SERVICE_URL = 'http://catalog:5001/books'  # Connect to Catalog Service to fetch books

@app.route('/')
def index():
    # Fetch all books from the Catalog Service
    response = requests.get(CATALOG_SERVICE_URL)
    books = response.json() if response.status_code == 200 else []
    
    return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

