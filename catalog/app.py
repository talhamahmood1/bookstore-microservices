from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__, static_folder='static')


# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        book_id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        price REAL NOT NULL,
                        stock INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/books', methods=['GET'])
def get_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = [{'book_id': row[0], 'title': row[1], 'price': row[2], 'stock': row[3]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        title = request.form['title']
        price = float(request.form['price'])
        stock = int(request.form['stock'])

        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (book_id, title, price, stock) VALUES (?, ?, ?, ?)',
                       (book_id, title, price, stock))
        conn.commit()
        conn.close()

        return 'Book added successfully! <a href="/add_book">Add another</a>'

    return render_template('add_book.html')

@app.route('/update_book', methods=['POST'])
def update_book():
    data = request.get_json()
    book_id = data['book_id']
    new_stock = data['stock']

    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET stock = ? WHERE book_id = ?', (new_stock, book_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Stock updated successfully'}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001)

