import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# Ensure debug server doesn't fail due to reload/import issues


def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    
    # Create main books table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            status TEXT DEFAULT 'Available',
            issued_to TEXT,
            issue_date TEXT,
            return_date TEXT
        )
    ''')
    
    # Create history table for tracking issues and returns
    conn.execute('''
        CREATE TABLE IF NOT EXISTS issue_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            book_title TEXT NOT NULL,
            issued_to TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            expected_return_date TEXT NOT NULL,
            returned_by TEXT,
            actual_return_date TEXT,
            status TEXT DEFAULT 'Active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    ''')
    
    # Add new columns if they don't exist
    try:
        conn.execute('ALTER TABLE books ADD COLUMN issue_date TEXT')
    except:
        pass
    
    try:
        conn.execute('ALTER TABLE books ADD COLUMN return_date TEXT')
    except:
        pass
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    
    # Get all books
    books = conn.execute('SELECT * FROM books').fetchall()
    
    # Get active issues (not yet returned)
    active_issues = conn.execute('''
        SELECT * FROM issue_history 
        WHERE status = 'Active'
        ORDER BY issue_date DESC
    ''').fetchall()
    
    # Get return history (completed)
    return_history = conn.execute('''
        SELECT * FROM issue_history 
        WHERE status = 'Returned'
        ORDER BY actual_return_date DESC
        LIMIT 20
    ''').fetchall()
    
    conn.close()

    return render_template('index.html', 
                         books=books, 
                         active_issues=active_issues,
                         return_history=return_history)


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO books (title, author) VALUES (?, ?)',
            (title, author)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_book.html')


@app.route('/issue/<int:book_id>', methods=['GET', 'POST'])
def issue_book(book_id):
    conn = get_db_connection()

    if request.method == 'POST':
        issued_to = request.form['issued_to']
        issue_date = request.form.get('issue_date', datetime.now().strftime('%Y-%m-%d'))
        return_date = request.form.get('return_date', (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'))

        # Get book title
        book = conn.execute('SELECT title FROM books WHERE id = ?', (book_id,)).fetchone()

        # Update book status
        conn.execute(
            '''
            UPDATE books
            SET status = ?, issued_to = ?, issue_date = ?, return_date = ?
            WHERE id = ?
            ''',
            ('Issued', issued_to, issue_date, return_date, book_id)
        )

        # Add to history
        conn.execute(
            '''
            INSERT INTO issue_history (book_id, book_title, issued_to, issue_date, expected_return_date, status)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (book_id, book['title'], issued_to, issue_date, return_date, 'Active')
        )

        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    book = conn.execute(
        'SELECT * FROM books WHERE id = ?',
        (book_id,)
    ).fetchone()

    conn.close()

    return render_template('issue_book.html', book=book)


@app.route('/return/<int:book_id>', methods=['GET', 'POST'])
def return_book(book_id):
    conn = get_db_connection()
    book = conn.execute(
        'SELECT * FROM books WHERE id = ?',
        (book_id,)
    ).fetchone()

    if request.method == 'POST':
        returned_by = request.form['returned_by']
        
        # Update book status
        conn.execute(
            '''
            UPDATE books
            SET status = ?, issued_to = NULL, issue_date = NULL, return_date = NULL
            WHERE id = ?
            ''',
            ('Available', book_id)
        )

        # Update history record
        conn.execute(
            '''
            UPDATE issue_history
            SET status = ?, returned_by = ?, actual_return_date = ?
            WHERE book_id = ? AND status = 'Active'
            ''',
            ('Returned', returned_by, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), book_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    conn.close()
    return render_template('return_book.html', book=book)


@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    conn = get_db_connection()

    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))


@app.route('/delete_history/<int:history_id>')
def delete_history(history_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM issue_history WHERE id = ?', (history_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/history')
def history():
    conn = get_db_connection()
    
    # Get all history records
    all_history = conn.execute('''
        SELECT * FROM issue_history 
        ORDER BY created_at DESC
    ''').fetchall()
    
    conn.close()
    return render_template('history.html', history=all_history)


import os

if __name__ == '__main__':
    init_db()

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host='0.0.0.0',
        port=port
    )