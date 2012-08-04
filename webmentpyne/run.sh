#/bin/sh
gunicorn -c unicorn.py web:app
