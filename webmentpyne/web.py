#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil, os, urlparse
from functools import wraps

from flask import Flask, jsonify, render_template, session

import mpris2
import settings

app = Flask(__name__)
app.debug = settings.DEBUG
app.secret_key = settings.SESSION_KEY

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

def sanitize_dict(dict_):
    """
        We need to strip ":" from dict keys as jinja seems to choke on these,
        also removing the "namspace" part as it seems irrelevant to me
    """

    def strip_prefix(item):
        if ':' not in item[0]:
            return item
        return item[0].split(':')[1], item[1]

    return dict(map(strip_prefix, dict_.iteritems()))


def inject_ifaces(f):
    """
        Adds player, tracklist and playlist interfaces to decorated func kwargs.
        If connection can't be established, returns JSON Response with False status.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            ifaces = mpris2.connect()
            kwargs.update(
                dict((var, val) for var, val in zip(('_player', '_tracklist', '_playlist'), ifaces)))
        except mpris2.DBusException, e:
            return jsonify(response=str(e), status=False)
        return f(*args, **kwargs)

    return decorated_function


def get_album_art(src):
    """
        We can't serve local files from any location, so let's
         cache it to our directory, if src is None serve default image
    """
    if not src:
        return 'nocover.jpg'

    parsed = list(urlparse.urlparse(src))
    parsed[0] = None
    file = os.path.basename(urlparse.urlunparse(parsed))
    tar = os.path.join(os.path.join(PROJECT_DIR, 'static', '.albumart'), file)
    shutil.copy(urlparse.urlunparse(parsed), tar)
    return file


@app.route('/')
def index():
    context = {'title': 'home', 'player': settings.PLAYER.split('.')[-1].capitalize()}
    return render_template('index.html', **context)


@app.route('/connection-error/')
def error():
    context = {'player': settings.PLAYER.split('.')[-1].capitalize()}
    return render_template('partials/connection_error.html', **context)


@app.route('/player/<action>/')
@app.route('/player/OpenUri/<path:uri>', defaults={'action': 'OpenUri'})
@inject_ifaces
def player_action(action, uri=None, **kwargs):
    resp = getattr(kwargs['_player'], action)() if not uri else getattr(kwargs['_player'], action)(uri)
    return jsonify(response=resp, status=True)


@app.route('/player/Volume/<direction>')
@inject_ifaces
def player_volume(direction, **kwargs):
    VOLUME_STEP = 0.1
    volume = kwargs['_player'].getAll()['Volume']
    if volume:
        session['old_volume'] = volume

    level = session['old_volume'] if volume == 0 else 0
    if direction == '+':
        level = volume + VOLUME_STEP
    elif direction == '-':
        level = volume - VOLUME_STEP
    resp = kwargs['_player'].setVolume(level)
    return jsonify(response=resp, status=True)


@app.route('/player/Shuffle/toggle')
@inject_ifaces
def player_shuffle(**kwargs):
    resp = kwargs['_player'].setShuffle(not kwargs['_player'].getAll()['Shuffle'])
    return jsonify(response=resp, status=True)


@app.route('/player/')
@inject_ifaces
def player_props(**kwargs):
    meta = kwargs['_player'].getAll()
    if meta['Metadata']:
        meta['Metadata']['mpris:artUrl'] = get_album_art(meta['Metadata'].get('mpris:artUrl', None))
    meta['html'] = render_template('partials/now_playing.html', **sanitize_dict(meta['Metadata']))
    return jsonify(response=meta, status=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')