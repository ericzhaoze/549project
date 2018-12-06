import sqlite3
import flask
import wordextractor


def dict_factory(cursor, row):
    output = {}
    for idx, col in enumerate(cursor.description):
        output[col[0]] = row[idx]
    return output

def get_db():
    if not hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db = sqlite3.connect(wordextractor.app.config['DATABASE_FILENAME'])
        flask.g.sqlite_db.row_factory = dict_factory
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")
    return flask.g.sqlite_db

@wordextractor.app.teardown_appcontext
def close_db(error):
    if hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db.commit()
        flask.g.sqlite_db.close()
