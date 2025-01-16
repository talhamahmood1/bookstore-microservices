from flask import Flask, request, render_template
import sqlite3
import requests

# Initialize the Flask app
app = Flask(__name__)

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
                    update_response = requests.post('http://catalog:5001/update_book', json={'book_id': book_id, 'stock': new_stock})

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

    # Fetch all books and orders to display in the form
    response = requests.get('http://catalog:5001/books')
    books = response.json() if response.status_code == 200 else []

    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = [{'id': row[0], 'customer_name': row[1], 'book_id': row[2], 'quantity': row[3]} for row in cursor.fetchall()]
    conn.close()
    
    return render_template('add_order.html', books=books, orders=orders)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
