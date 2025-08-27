from app import app
from flask import render_template


import sqlite3

@app.route('/cart')
def cart():
    connection = sqlite3.connect('nithStore_database.sqlite3')
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
    return render_template('cart.html', products=products, erorr='')
