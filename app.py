# M. Indra Ardian Saputra
# 20240140160
# D


import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_NAME = "books.db"

def connectdb():
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db_Pengguna():
    conn = connectdb()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama VARCHAR(100) NOT NULL,
            nim INTEGER NOT NULL,
            email VARCHAR(100) NOT NULL
        )
""")
    conn.commit()
    conn.close()

def init_db_Peminjam():
    conn = connectdb()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama VARCHAR(100) NOT NULL,
            judul_buku VARCHAR(100) NOT NULL,
            tanggal_pinjam DATE NOT NULL,
            status_peminjaman VARCHAR(50) NOT NULL
        )
""")
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = connectdb()
    books = conn.execute("SELECT * FROM books"). fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nama = request.form['nama']
        id = request.form['id']
        judul = request.form['judul']
        peminjam = request.form['peminjam']
        tanggal_pinjam = request.form['tanggal.pinjam']

        conn = connectdb()
        conn.execute(
            "INSERT INTO books (nama, id, judul, peminjam, tanggal_pinjam) VALUES (?, ?)",
            (nama, id, judul, peminjam, tanggal_pinjam)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = connectdb()
    book = conn.execute(
        "SELECT * FROM books WHERE id = ?", (id,)
    ).fetchall()

    if not book:
        return "Buku tidak ditemukan", 404

    if request.method == 'POST':
        nama = request.form['nama']
        id = request.form['id']
        judul = request.form['judul']
        peminjam = request.form['peminjam']
        tanggal_pinjam = request.form['tanggal.pinjam']
        conn.execute(
            "UPDATE books SET nama = ?, id = ?, judul = ?, peminjam = ?, tanggal_pinjam = ? WHERE id = ?",
            (nama, id, judul, peminjam, tanggal_pinjam, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('edit.html', book=book)

@app.route('/delete/<int:id>')
def delete(id):
    conn = connectdb()
    conn.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    init_db_Peminjam()
    app.run(host="0.0.0.0", port=5000, debug=True)