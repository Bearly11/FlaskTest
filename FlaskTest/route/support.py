from app import app
from flask import render_template
import requests


@app.route('/support')
def support():
    return render_template('support.html')