from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__, static_folder='static')

# Initialize SQLite database
def init_db():
    with sqlite3.connect('books.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                            book_id INTEGER PRIMARY KEY,
                            title TEXT NOT NULL,
                            price REAL NOT NULL,
                            stock INTEGER NOT NULL)''')
        conn.commit()

@app.route('/books', methods=['GET'])
def get_books():
    with sqlite3.connect('books.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = [{'book_id': row[0], 'title': row[1], 'price': row[2], 'stock': row[3]} for row in cursor.fetchall()]
    return jsonify(books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        try:
            book_id = int(request.form['book_id'])
            title = request.form['title']
            price = float(request.form['price'])
            stock = int(request.form['stock'])

            with sqlite3.connect('books.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO books (book_id, title, price, stock) VALUES (?, ?, ?, ?)',
                               (book_id, title, price, stock))
                conn.commit()
            return 'Book added successfully! <a href="/add_book">Add another</a>'
        except Exception as e:
            return f'Error: {e}', 400

    return render_template('add_book.html')

@app.route('/update_book', methods=['POST'])
def update_book():
    try:
        book_id = int(request.form['book_id'])
        new_title = request.form.get('title')
        new_price = request.form.get('price')
        new_stock = request.form.get('stock')

        with sqlite3.connect('books.db') as conn:
            cursor = conn.cursor()
            if new_title:
                cursor.execute('UPDATE books SET title = ? WHERE book_id = ?', (new_title, book_id))
            if new_price:
                cursor.execute('UPDATE books SET price = ? WHERE book_id = ?', (float(new_price), book_id))
            if new_stock:
                cursor.execute('UPDATE books SET stock = ? WHERE book_id = ?', (int(new_stock), book_id))
            conn.commit()
        return 'Book updated successfully! <a href="/add_book">Go Back</a>'
    except Exception as e:
        return f'Error: {e}', 400

@app.route('/delete_book', methods=['POST'])
def delete_book():
    try:
        book_id = int(request.form['book_id'])
        with sqlite3.connect('books.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
            conn.commit()
        return 'Book deleted successfully! <a href="/add_book">Go Back</a>'
    except Exception as e:
        return f'Error: {e}', 400

@app.route('/delete_all_books', methods=['POST'])
def delete_all_books():
    try:
        with sqlite3.connect('books.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM books')
            conn.commit()
        return 'All books deleted successfully! <a href="/add_book">Go back</a>'
    except Exception as e:
        return f'Error: {e}', 400

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001)
