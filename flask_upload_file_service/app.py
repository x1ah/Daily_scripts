#!/usr/bin/env python
# encoding: utf-8

import os

from flask import (Flask, request, flash, redirect, send_from_directory,
                   render_template, url_for)
from flask_uploads import UploadSet, configure_uploads, patch_request_class, ALL
from werkzeug import SharedDataMiddleware

basedir = os.getcwd()
app = Flask(__name__)
app.config['UPLOADED_FILES_DEST'] = os.path.join(basedir, 'uploads')
app.config['FILE_PATH'] = os.path.join(basedir, 'uploads')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'ouahflnl'

upload_file = UploadSet('files', ALL)
configure_uploads(app, upload_file)
patch_request_class(app, 5*1024*1024*1024*1024)


@app.route("/file/<filename>", build_only=True)
def prev_file(filename):
    return send_from_directory(app.config.get('UPLOADED_FILES_DEST'), filename)


app.wsgi_app = SharedDataMiddleware(
    app.wsgi_app,
    {
        "/file": app.config.get("UPLOADED_FILES_DEST")
    },
    cache=False
)


@app.route("/")
def index():
    allfiles = os.listdir(app.config.get('UPLOADED_FILES_DEST'))
    return render_template('index.html', file_lst_view=allfiles)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        filename = upload_file.save(request.files.get('file'))
        url = upload_file.url(filename)
        return redirect(url_for(".index"))
    else:
        return render_template("upload.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
