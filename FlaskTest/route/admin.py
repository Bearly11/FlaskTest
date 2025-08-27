from itertools import product

from unicodedata import category

from app import app
from flask import render_template, request
import requests


import sqlite3
from flask import redirect, url_for


def db():
    conn = sqlite3.connect('nithStore_database.sqlite3')
    conn.row_factory = sqlite3.Row  # <-- lets you use row["field"]
    return conn


@app.route('/admin', methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == '123':
            return adminProducts()
        else:
            return render_template('admin/login.html', error='Invalid username or password')

    return render_template('admin/login.html')


@app.route('/admin/products')
def adminProducts():
    connection = db()
    cursor = connection.cursor()
    result = cursor.execute('SELECT * FROM products').fetchall()
    products = []
    for item in result:
        product = {
            'id': item[0],
            'title': item[1],
            'category': item[2],
            'price': item[3],
            'image': item[4],
            'description': item[5],

        }
        products.append(product)
    return render_template('admin/admin.html', products=products, erorr='')

@app.get("/admin/products/search")
def search_product():
    q = (request.args.get("q") or "").strip().lower()
    products = []

    conn = db()
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
                "title": item[1],
                "category": item[2],
                "price": item[3],
                "image": item[4],
                'description': item[5],

            })

    return render_template("admin/admin.html", q=q, products=products)


@app.route("/admin/products/new", methods=["GET", "POST"])
def admin_new_product():
    if request.method == "POST":
        name = (request.form.get("title") or "").strip()
        category = (request.form.get("category") or "").strip()
        image = (request.form.get("image") or "").strip()
        description = (request.form.get("description") or "").strip()
        try:
            price = float(request.form.get("price") or 0)
        except ValueError:
            price = 0.0

        if not name or not category or price <= 0:
            return render_template("admin/add_product.html", error="Please fill all fields correctly.")

        with db() as conn:
            conn.execute(
                """
                INSERT INTO products (name, category, price, image, description)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, category, price, image, description),
            )
            conn.commit()
        return render_template("admin/add_product.html", success="Product added successfully.")

    return render_template("admin/add_product.html")


def find_product(pid):
    with db() as conn:
        return conn.execute('SELECT * FROM products WHERE id = ?', (pid,)).fetchone()

@app.route("/admin/products/<int:pid>/update", methods=["GET", "POST"])
def admin_update_product(pid):
    row = find_product(pid)
    if not row:
        return render_template("admin/update_product.html", error="Product not found.")

    product = {
        "id": row["id"],
        "name": row["name"],
        "category": row["category"],
        "price": row["price"],
        "image": row["image"],
        "description": row["description"],
    }

    if request.method == "POST":
        name = (request.form.get("name") or request.form.get("title") or "").strip()
        category = (request.form.get("category") or "").strip()
        image = (request.form.get("image") or "").strip()
        description = (request.form.get("description") or "").strip()
        try:
            price = float(request.form.get("price") or 0)
        except ValueError:
            price = 0.0

        if not name or not category or price <= 0:
            return render_template("admin/update_product.html", error="Please fill all fields correctly.")

        with db() as conn:
            conn.execute(
                f"UPDATE products SET name=?, category=?, price=?, image=?, description=? WHERE id=?",
                (name, category, price, image, description, pid),
            )
            conn.commit()
        return render_template("admin/update_product.html", success="Product update successfully.", product=product)

    return render_template("admin/update_product.html", product=product)

@app.route("/admin/products/<int:pid>/delete", methods=["POST"])
def admin_delete_product(pid):
    with db() as conn:
        conn.execute("DELETE FROM products WHERE id=?", (pid,))
        conn.commit()
    return redirect(url_for("adminProducts"))
