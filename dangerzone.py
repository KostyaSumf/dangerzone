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
    key = None
    admin = False

    def __init__(self):
        players.append(self)


app = Flask(__name__)


@app.route('/')
def hello():
    """
     Redirects to the static index page, which should be customized to your brand's liking.
     It is recommended to place the client under /play, where the default coffeescript one is, but this can be
     changed.
    """
    return redirect(url_for('static', filename='index.html'))


@app.route('/admin')
def admin():
    """
    Will serve an admin page if player is an admin.
    """
    admin = checkAdminAuth(request.cookies.get('dzAuthKey'))
    if admin:
        return "Authenticated."
    else:
        return Response(response="Invalid request. Either you have no authentication token in your cookies,"
                                 "your key is not a valid player, or that player is not an admin.", status=400)


def checkAdminAuth(key):
    """
    This returns true only if:
    * host computer has a cookie identifying it as authed (which should be passed as :param key:)
    * the auth key is actually a player
    * the auth key's player is an admin

    Alternatively they can reach each different admin function via /admin/*, which will run through this function.

    :rtype boolean:
    """
    if key:
        if keys.has_key(key):  # TODO: What is "in" and how does it replace "has_key"?
            player = keys[key]
            if player.admin:
                return True  # TODO: Return a static page only by python function?
            else:
                return False
        else:
            return False
    else:
        return False

if __name__ == '__main__':
    master_user = str(os.environ.get('DZONE_MASTER_USER'))
    master_pass = str(os.environ.get('DZONE_MASTER_PASS'))
    if master_user == "" or master_pass == "" or master_user is None or master_pass is None:
        print "No master user or password given."
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)