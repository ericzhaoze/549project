import os
import shutil
import tempfile
import hashlib
import flask
from flask import request, redirect, url_for, session, abort
import arrow
import wordextractor
import time

from flask import Flask, current_app
# All module pre-load
app = Flask(__name__)
with app.app_context():
    shared_module = 1


@wordextractor.app.route('/', methods=['GET', 'POST'])
def show_index():
    context = {}
    context["Default"] = ""
    context["listword"] = "[]"
    context["type"] = 0
    context["mytopic"] = ""
    if request.method == 'POST':
        text = request.form['text']
        topic = request.form['topic']
        context["mytopic"] = topic
        if text != "":
            context["type"] = 1
            context["Default"] = text
            context["listword"] = "[{\"text\":\"study\",\"size\":40},{\"text\":\"motion\",\"size\":15},{\"text\":\"forces\",\"size\":10}]"
    return flask.render_template("index.html", **context)



