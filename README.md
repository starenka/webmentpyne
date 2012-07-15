## Wha?

Webmentpyne is a simple web interface for [Clementine](http://www.clementine-player.org/about) player using [MPRIS2](http://specifications.freedesktop.org/mpris-spec/latest/) interface via [D-Bus](http://www.freedesktop.org/wiki/Software/dbus). It allows you to control Clementine (or maybe later on any other player supporting MPRIS2 via D-Bus - f.e. Rhythmbox, Banshe, Amarok...) from your browser. For now, it's being tested just against Clementine 1.0.1.

Motivation behind this "project" was to allow me control my [Rasberry Pi](http://www.raspberrypi.org/) based audio system with my cellphone or laptop. Nevertheless it could be used in zillion other cases.

It's just a simle webapp skeleton returning JSON now (the MPRIS2 wrapper needs some love too). I need to do all the HTML/CSS/JS mayhem to make it usable via browser. Just take a look:

 ![screenshot](https://github.com/starenka/webmentpyne/blob/master/screenshot.png)

or fire up the app to check yourself:


    starenka /tmp % git clone git://github.com/starenka/webmentpyne.git
    Cloning into 'webmentpyne'...
    remote: Counting objects: 176, done.
    remote: Compressing objects: 100% (139/139), done.
    remote: Total 176 (delta 71), reused 124 (delta 19)
    Receiving objects: 100% (176/176), 107.78 KiB, done.
    Resolving deltas: 100% (71/71), done.
    starenka /tmp % cd webmentpyne
    starenka /tmp/webmentpyne % virtualenv .env
    New python executable in .env/bin/python
    Installing setuptools............done.
    Installing pip...............done.
    starenka /tmp/webmentpyne % source .env/bin/activate
    (.env)starenka /tmp/webmentpyne % pip install requirements.pip
    ....... this will take a while ........
    (.env)starenka /tmp/webmentpyne % python webmentpyne/web.py
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader

I'd like to implement some Playlist and Tracklist features in the future. Feel free to help me out!