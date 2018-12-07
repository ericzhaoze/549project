import os
import shutil
import tempfile
import hashlib
import flask
from flask import request, redirect, url_for, session, abort
import arrow
import wordextractor
import time
import gensim.downloader as api
import interface



from flask import Flask, current_app
# All module pre-load
app = Flask(__name__)
with app.app_context():
    print("Loading pretrained model...")
    shared_module = api.load("glove-twitter-25")
    print("Model loaded.")


@wordextractor.app.route('/', methods=['GET', 'POST'])
def show_index():
    print(os.getcwd())
    trainDir = '../../EmailSummarizationKeywordExtraction/CorporateSingleXML/'
    testDir = '../../EmailSummarizationKeywordExtraction/smallTest/'
    em = interface.ExtractManager(trainDir, testDir, shared_module)

    context = {}
    context["Default"] = ""
    context["listword"] = "[]"
    context["type"] = 0
    context["wordcount"] = 5
    context["mytopic"] = ""
    if request.method == 'POST':
        text = request.form['text']
        topic = request.form['topic']
        context["mytopic"] = topic
        if request.form["wordcount"] != "":
            context["wordcount"] = int(request.form["wordcount"])
        if text != "":
            context["type"] = 1
            context["Default"] = text
            if topic == "":
                topic = None
            # context["listword"] = "[{\"text\":\"study\",\"size\":40},{\"text\":\"motion\",\"size\":15},{\"text\":\"forces\",\"size\":10}]"
            context["listword"] = em.output_serializer(em.extract_keywords(topic_words = topic,threads = list([text]), keyword_number = context["wordcount"]))
            

    return flask.render_template("index.html", **context)



