import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import basedir
from flaskext.markdown import Markdown

app = Flask('partsdb')
app.config.from_object('config')
db = SQLAlchemy(app)
Markdown(app)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/partsdb.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('PartsDB Startup...')

from partsdb import views, models, filters
