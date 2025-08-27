from app import app
from flask import render_template
import sqlite3

def fetch_products(query="SELECT * FROM products", params=()):
    with sqlite3.connect("nithStore_database.sqlite3") as conn:
        cur = conn.cursor()
        rows = cur.execute(query, params).fetchall()
    return [
        {"id": r[0], "title": r[1], "category": r[2], "price": r[3], "image": r[4], "description": r[5]}
        for r in rows
    ]

@app.route("/")
@app.route("/home")
def home():
    products = fetch_products("SELECT * FROM products ORDER BY id DESC")
    featured = fetch_products("SELECT * FROM products WHERE price > ? ORDER BY id DESC LIMIT 4", (900,))
    return render_template("home.html", products=products, featured=featured)
