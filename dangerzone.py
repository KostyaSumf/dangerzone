"""
This is the main file. It will take private information from environment variables. You will need to have two enviroment
variables: 'DZONE_MASTER_USER', the master username, and 'DZONE_MASTER_PASS', the master password.
"""

__author__ = 'alasershark'

import os
import random
import hashlib
import base64
import json
from flask import Flask, redirect, url_for, Response, request, render_template

players = []
keys = {}
usernames = {}
world = {}
cities = {}

# scroll to the bottom for a table of contents.


class Player:

    key = None
    admin = False
    username = None
    password = None
    cities = []

    def __init__(self, username, password, admin):
        players.append(self)
        self.username = username
        usernames[username] = self
        self.password = password
        self.admin = admin
        key = self.generateKey()
        keys[key] = self
        self.key = key

    def generateKey(self):
        bits = str(random.getrandbits(256))
        hashed = hashlib.sha256(bits)
        encoded = base64.b64encode(hashed.digest(), "dZ").rstrip("==")
        return encoded


class Link:

    url = None
    name = None
    
    def __init__(self, home, name):
        self.url = home + "/" + name
        self.name = name


class Building:

    x = None
    y = None
    btype = None
    owner = None

    def __init__(self, x, y, btype, owner):
        self.btype = btype
        self.x = x
        self.y = y
        self.owner = owner
        if not x in world:
            world[x] = {}
        if not y in world[x]:
            world[x][y] = self
        else:
            raise Exception('already a building there')

    def getData(self):
        return {'type': self.btype,
                'owner': self.owner}


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
        links = [Link("admin", "stop")]
        return render_template('links.html', links=links, title='Dangerzone Administation')
    else:
        return Response(response="Invalid request. Either you have no authentication token in your cookies, "
                                 "your key is not a valid player, or that player is not an admin.", status=400)


@app.route('/api/account/login', methods=['POST'])
def login():
    """
    If the player has correct login credentials, gives them a cookie with their key in it.
    """
    j_son = str(request.data)
    # print j_son
    stuff = json.loads(j_son)
    if getPlayerKey(str(stuff['user']), str(stuff['password'])):
        resp = Response(content_type='application/json', status=200, response=json.dumps({"success": True}))
        resp.set_cookie('dzAuthKey', getPlayerKey(str(stuff['user']), str(stuff['password'])))
        return resp
    return Response(response='Invalid credentials and/or improperly formatted credentials.', status=403)


@app.route('/api/account/make', methods=['POST'])
def makeAccount():
    """
    Generates an account with the given credentials.
    """
    jsson = str(request.data)
    stuff = json.loads(jsson)
    player = Player(str(stuff['user']), str(stuff['password']), False)
    return Response(content_type='application/json', status=200, response=json.dumps({"user": player.username,
                                                                                      "password": player.password}))


@app.route('/api/world/tile', methods=['POST'])
def getTile():
    """
    Fetches the tile with the given coordinates
    """
    jsson = str(request.data)
    stuff = json.loads(jsson)
    if not stuff.get('x') and stuff.get('y'):
        return Response(response=400)
    elif stuff['x'] in world and stuff['y'] in world['x']:
        return Response(content_type='application/json', status=200,
                        response=json.dumps(world[stuff['x']][stuff['y']].getData()))
    else:
        return Response(response=204)


@app.route('api/world/city', methods=['POST'])
def getCity():
    """
    Fetches the tiles that a certain city contains, along with the cities owner.
    """
    jsson = str(request.data)
    stuff = json.loads(jsson)



def checkAdminAuth(key):
    """
    This returns true only if:
    * host computer has a cookie identifying it as authed (which should be passed as :param key:)
    * the auth key is actually a player
    * the auth key's player is an admin

    :rtype boolean:
    """
    if key:
        if key in keys:
            player = keys[key]
            if player.admin:
                return True
    return False


def checkPlayerKey(key):
    """
    Same as checkAdminAuth, only without the admin check.

    :rtype boolean:
    """

    if key:
        if key in keys:
            return True
    return False


def getPlayerKey(user, password):
    """
    Returns a player's authkey, given their username and password.
    """
    if not user in usernames:
        return None
    player = usernames.get(user)
    if player and player.password == password:
        return player.key
    return None


if __name__ == '__main__':
    master_user = os.environ.get('DZONE_MASTER_USER')
    master_pass = os.environ.get('DZONE_MASTER_PASS')
    if master_user == "" or master_pass == "" or master_user is None or master_pass is None:
        print "No master user or password given."
        print "Using default user and password - You should change these ASAP."
        Player("oogooly", "boogooly", True)
    else:
        print "A master user and password were given."
        Player(master_user, master_pass, True)
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)

# Have fun coding! - sharky