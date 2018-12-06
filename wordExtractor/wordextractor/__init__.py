import flask

app = flask.Flask(__name__) 
app.config.from_object('wordextractor.config')
app.config.from_envvar('WORDEXTRACTOR_SETTINGS', silent=True)
import wordextractor.views  
import wordextractor.model  
