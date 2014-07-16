#!/usr/bin/env python

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import basedir
from flaskext.markdown import Markdown

app = Flask('partsdb')
app.config.from_object('config')
db = SQLAlchemy(app)
Markdown(app)

from partsdb import views, models, filters
