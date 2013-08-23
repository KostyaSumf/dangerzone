"""
This is the main file. It will take private information from environment variables. You will need to have two enviroment
variables: 'DZONE_MASTER_USER', the master username, and 'DZONE_MASTER_PASS', the master password.
"""

__author__ = 'alasershark'

import os
from flask import Flask, redirect, url_for, Response, request

players = []
keys = {}


class Player:

    def __init__(self):
        players.append(self)



app = Flask(__name__)


@app.route('/')
def hello():
    return redirect(url_for('static', filename='index.html'))

@app.route('/api/players', methods=['POST'])
def getPlayers():
    key = None
    try:
        key = request.headers['apiKey']
    except KeyError:
        return Response(response='No key provided.', status=403)
    return Response(status=500, mimetype='application/json')

if __name__ == '__main__':
    master_user = os.environ['DZONE_MASTER_USER']
    master_pass = os.environ['DZONE_MASTER_PASS']
    keys[master_user] = master_pass
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)