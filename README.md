## Wha?

Webmentpyne is a simple web interface for [Clementine](http://www.clementine-player.org/about) player using [MPRIS2](http://specifications.freedesktop.org/mpris-spec/latest/) interface via [D-Bus](http://www.freedesktop.org/wiki/Software/dbus). It allows you to control Clementine (or maybe later on any other player supporting MPRIS2 via D-Bus - f.e. Amarok) from your browser. For now, it's being tested just against Clementine 1.0.1.

Motivation behind this "project" was to allow me control my [Rasberry Pi](http://www.raspberrypi.org/) based audio system with my cellphone or laptop. Nevertheless it could be used in zillion other cases.

It's just a simle webapp skeleton returning JSON now (the MPRIS2 wrapper needs some love too). I need to do all the HTML/CSS/JS mayhem to make it usable via browser. Just take a look. Fire up the app:

    (webmentpyne)starenka /prac/python/webmentpyne % python webmentpyne/web.py
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader

to get player stats try:

    starenka /tmp % curl http://127.0.0.1:5000/player/
    {
      "status": 200,
      "response": {
        "CanGoNext": 1,
        "CanPause": 1,
        "Shuffle": 0,
        "CanControl": 1,
        "LoopStatus": "Playlist",
        "PlaybackStatus": "Playing",
        "Volume": dbus.Double(0.9, variant_level=1),
        "MinimumRate": dbus.Double(1.0, variant_level=1),
        "Rate": dbus.Double(1.0, variant_level=1),
        "CanPlay": 1,
        "Position": 195179351,
        "CanSeek": 1,
        "CanGoPrevious": 1,
        "Metadata": {
          "xesam:album": "The Lucid Effect",
          "xesam:useCount": 1,
          "xesam:title": "Winks jazz",
          "xesam:trackNumber": 8,
          "xesam:artist": [
            "40 Winks"
          ],
          "xesam:genre": [
            "Hip-Hop"
          ],
          "mpris:trackid": "/org/mpris/MediaPlayer2/Track/25",
          "mpris:length": 199000000,
          "mpris:artUrl": "file:///tmp/clementine-art-C24958.jpg",
          "xesam:autoRating": 50,
          "xesam:contentCreated": "2011-04-21T10:30:45",
          "xesam:lastUsed": "2012-02-23T14:08:13",
          "xesam:url": "file:///data/mp3/40 Winks/The Lucid Effect [2008]/08_-_Winks jazz.mp3"
        },
        "MaximumRate": dbus.Double(1.0, variant_level=1)
      }
    }

control the player (Play, Pause, Next.... you name it) in a jiffy:

    starenka /tmp % curl http://127.0.0.1:5000/player/Pause/
    {
      "status": 200,
      "response": null
    }

    starenka /tmp % curl http://127.0.0.1:5000/player/OpenUri/http://www.starenka.net/pub/vltavarmx.mp3
    {
      "status": 200,
      "response": null
    }

    starenka /tmp % curl http://127.0.0.1:5000/player/
    {
      "status": 200,
      "response": {
        "CanGoNext": 1,
        "CanPause": 1,
        "Shuffle": 0,
        "CanControl": 1,
        "LoopStatus": "Playlist",
        "PlaybackStatus": "Playing",
        "Volume": dbus.Double(0.9, variant_level=1),
        "MinimumRate": dbus.Double(1.0, variant_level=1),
        "Rate": dbus.Double(1.0, variant_level=1),
        "CanPlay": 1,
        "Position": 5015513,
        "CanSeek": 0,
        "CanGoPrevious": 1,
        "Metadata": {
          "xesam:album": "vltava rmx (bedrich smetana)",
          "xesam:title": "http://www.starenka.net/pub/vltavarmx.mp3",
          "xesam:artist": [
            "starenka"
          ],
          "mpris:trackid": "/org/mpris/MediaPlayer2/Track/68",
          "mpris:artUrl": "file:///tmp/clementine-art-L24958.jpg",
          "xesam:url": "http://www.starenka.net/pub/vltavarmx.mp3"
        },
        "MaximumRate": dbus.Double(1.0, variant_level=1)
      }
    }

I'd like to implement more Playlist and Tracklist features in the future. Feel free to help me out!