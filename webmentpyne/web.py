#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps

from flask import Flask, jsonify, render_template, json

import clementine

app = Flask(__name__)
app.debug = True

def inject_ifaces(f):
    """
        Adds player, tracklist and playlist interfaces to decorated func kwargs.
        If connection can't be established, returns JSON Response with 500 status.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            ifaces = clementine.connect()
            kwargs.update(
                dict((var, val) for var, val in zip(('_player', '_tracklist', '_playlist'), ifaces)))
        except clementine.DBusException, e:
            return jsonify(response=str(e), status=500)
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    context = {'title': 'home'}
    return render_template('index.html', **context)


@app.route('/player/<action>/')
@app.route('/player/OpenUri/<path:uri>', defaults={'action': 'OpenUri'})
@inject_ifaces
def player_action(action, uri=None, **kwargs):
    ACTIONS = ('Next', 'Pause', 'Play', 'PlayPause', 'Previous', 'Stop', 'OpenUri')
    if action not in ACTIONS:
        mess = 'Not supported player method. Supported methods: %s' % ', '.join(ACTIONS)
        return jsonify(response=mess, status=400)
    resp = getattr(kwargs['_player'], action)() if not uri else getattr(kwargs['_player'], action)(uri)
    #return getAll or just subset instead of None?
    return jsonify(response=resp, status=200)


def _sanitize_dict(dict_):
    """
    we need to strip ":" from dict keys as jinja seems to choke on these,
    also removing the "namspace" part as it seems irrelevant to me
    """

    def strip_prefix(item):
        if ':' not in item[0]:
            return item
        return item[0].split(':')[1], item[1]

    return dict(map(strip_prefix, dict_.iteritems()))


@app.route('/player/')
@inject_ifaces
def player_props(**kwargs):
    meta = kwargs['_player'].getAll()
    meta['html'] = render_template('partials/now_playing.html', **_sanitize_dict(meta['Metadata']))
    return jsonify(response=meta, status=200)

if __name__ == '__main__':
    app.run()