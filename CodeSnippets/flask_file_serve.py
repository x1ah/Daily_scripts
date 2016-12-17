#!/usr/bin/env python
# encoding: utf-8

# official document: http://flask.pocoo.org/docs/0.10/patterns/fileuploads/

from flask import Flask, send_from_directory
from werkzeug import SharedDataMiddleware

app = Flask(__name__)

app.config["FILE_PATH"] = "."   # The path want handdle

def prev_file(filename):
    return send_from_directory(app.config.get("FILE_PATH"), filename)

app.add_url_rule("/file/<filename>", "prev_file", build_only=True)

app.wsgi_app = SharedDataMiddleware(
    app.wsgi_app,
    {
        "/file": app.config.get("FILE_PATH")
    },
    cache = False
    # tips: http://stackoverflow.com/questions/11515804/zombie-shareddatamiddleware-on-python-heroku
)


if __name__ == "__main__":
    app.run()
