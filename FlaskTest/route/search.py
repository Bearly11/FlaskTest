from app import app
from flask import render_template, request
import sqlite3


@app.get("/search")
def search():
    q = (request.args.get("q") or "").strip().lower()
    products = []

    conn = sqlite3.connect("nithStore_database.sqlite3")
    cursor = conn.cursor()

    if q:

        result = cursor.execute(
            """
            SELECT * FROM products WHERE LOWER(REPLACE(name, ' ', '')) LIKE LOWER(REPLACE(? , ' ', ''))
               OR LOWER(REPLACE(category, ' ', '')) LIKE LOWER(REPLACE(? , ' ', ''))
            """,
            (f"%{q}%", f"%{q}%")
        ).fetchall()

        for item in result:
            products.append({
                "id": item[0],
                "name": item[1],
                "category": item[2],
                "price": item[3],
                "image": item[4],
                'description': item[5],

            })

    return render_template("search.html", q=q, products=products)
