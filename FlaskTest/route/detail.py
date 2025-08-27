from app import app
from flask import render_template
import requests

import sqlite3

# @app.route('/detail')
# def detail():
#     product = []
#     error = ''
#     pro_id = request.args.get("pro_id")
#     if pro_id:
#         try:
#             r = requests.get(f'https://fakestoreapi.com/products/{pro_id}')
#             if r.status_code == 200:
#                 product = r.json()
#
#         except Exception as e:
#             error = str(e)
#     else:
#         error = 'Query erorr'
#
#     return render_template('detail.html', product=product, error=error)


@app.route('/detail/<int:pro_id>')
def detail(pro_id):
    product = []
    connection = sqlite3.connect('nithStore_database.sqlite3')
    cursor = connection.cursor()
    result = cursor.execute(f'SELECT * FROM products where id ={pro_id}').fetchone()
    if result:
        product = {
            'id': result[0],
            'title': result[1],
            'category': result[2],
            'price': result[3],
            'image': result[4],
            'description': result[5],
        }

    return render_template('detail.html', product=product, erorr='')
