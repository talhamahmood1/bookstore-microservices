from flask import Flask, request, render_template, jsonify
import requests
import sqlite3

app = Flask(__name__, static_folder='static')


CATALOG_SERVICE_URL = 'http://catalog:5001/update_book'
ORDERS_SERVICE_URL = 'http://order:5002/orders'

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_name TEXT NOT NULL,
                        book_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        customer_name = request.form['name']
        book_id = int(request.form['book_id'])
        quantity = int(request.form['quantity'])

        # Fetch all books from Catalog
        response = requests.get('http://catalog:5001/books')
        if response.status_code == 200:
            books = response.json()

            # Find the book with the given book_id
            book = next((b for b in books if b['book_id'] == book_id), None)
            
            if book:
                if book['stock'] >= quantity:
                    # Decrease stock and place the order
                    new_stock = book['stock'] - quantity
                    update_response = requests.post(CATALOG_SERVICE_URL, json={'book_id': book_id, 'stock': new_stock})

                    if update_response.status_code == 200:
                        conn = sqlite3.connect('orders.db')
                        cursor = conn.cursor()
                        cursor.execute('INSERT INTO orders (customer_name, book_id, quantity) VALUES (?, ?, ?)',
                                       (customer_name, book_id, quantity))
                        conn.commit()
                        conn.close()

                        return 'Order placed successfully! <a href="/add_order">Place another</a>'
                    else:
                        return f'Failed to update stock for Book ID {book_id}. <a href="/add_order">Try again</a>'
                else:
                    return f'Insufficient stock for Book ID {book_id}. <a href="/add_order">Try again</a>'
            else:
                return f'Invalid Book ID {book_id}. <a href="/add_order">Try again</a>'
        else:
            return 'Failed to fetch books from Catalog. <a href="/add_order">Try again</a>'

    # Fetch all books to display in the form
    response = requests.get('http://catalog:5001/books')
    books = response.json() if response.status_code == 200 else []
    
    return render_template('add_order.html', books=books)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002)

