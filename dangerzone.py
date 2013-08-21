"""
This is the main file. It will take private information from environment variables.
"""

__author__ = 'alasershark'

import os
from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route('/')
def hello():
    return redirect(url_for('static', filename='index.html'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)