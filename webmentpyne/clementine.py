#!/usr/bin/env python
import collections
from functools import partial

import dbus
from dbus.exceptions import DBusException

import settings

session_bus = dbus.SessionBus()

def get_partial(iface_prop, iface_path, property):
    return convert_to_pytypes(iface_prop.Get(iface_path, property))


def get_all_partial(iface_prop, iface_path):
    return convert_to_pytypes(iface_prop.GetAll(iface_path))


def set_partial(iface_prop, iface_path, property, value=None):
    return iface_prop.Set(iface_path, property, value)


def connect():
    PATH_IFACE_PLAYER = 'org.mpris.MediaPlayer2.Player'
    PATH_IFACE_TRACKLIST = 'org.mpris.MediaPlayer2.TrackList'
    PATH_IFACE_PLAYLIST = 'org.mpris.MediaPlayer2.PlayList'

    try:
        program = session_bus.get_object(settings.PLAYER, '/org/mpris/MediaPlayer2')
        iface_player = dbus.Interface(program, dbus_interface=PATH_IFACE_PLAYER)
        iface_tracklist = dbus.Interface(program, dbus_interface=PATH_IFACE_TRACKLIST)
        iface_playlist = dbus.Interface(program, dbus_interface=PATH_IFACE_PLAYLIST)
        iface_prop = dbus.Interface(program, "org.freedesktop.DBus.Properties")

        #make methods to get/set ifaces' properties to avoid dbus clumsiness
        # qdbus org.mpris.MediaPlayer2.clementine /org/mpris/MediaPlayer2 | grep 'property read'
        for one in ('Metadata', 'Volume', 'LoopStatus', 'PlaybackStatus', 'Position', 'Shuffle'):
            setattr(iface_player, 'get%s' % one, partial(get_partial, iface_prop, iface_player.dbus_interface, one))
        for one in ('Volume', 'Shuffle', 'LoopStatus'):
            setattr(iface_player, 'set%s' % one, partial(set_partial, iface_prop, iface_player.dbus_interface, one))

        for one in ('Tracks',):
            setattr(iface_tracklist, 'get%s' % one,
                partial(get_partial, iface_prop, iface_tracklist.dbus_interface, one))

        #get_All methods for easy properties extractions
        for one in (iface_player, iface_playlist, iface_tracklist):
            setattr(one, 'getAll', partial(get_all_partial, iface_prop, one.dbus_interface))

        return iface_player, iface_tracklist, iface_playlist
    except DBusException:
        raise


def convert_to_pytypes(data):
    """
    converts dbus monstrosities back to python types
    """
    if isinstance(data, dbus.String):
        return unicode(data)
    elif isinstance(data, dbus.Double):
        return float(data)
    elif isinstance(data, dbus.Boolean):
        return bool(data)
    elif isinstance(data, (dbus.Int16, dbus.Int32, dbus.Int64)):
        return int(data)
    elif isinstance(data, (collections.Mapping, dbus.Dictionary)):
        return dict(map(convert_to_pytypes, data.iteritems()))
    elif isinstance(data, (collections.Iterable, dbus.Array)):
        return map(convert_to_pytypes, list(data))
    else:
        return data

if __name__ == '__main__':
    iface_player, iface_tracklist, iface_playlist = connect()

    import pprint
    pprint.pprint(iface_player.getAll())