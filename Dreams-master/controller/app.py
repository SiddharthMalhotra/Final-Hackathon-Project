from flask import Flask, render_template, request, abort, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

from flask_pymongo import PyMongo
from flask import jsonify
from decimal import Decimal
import math
from account_api import account_api

import os
import sys

DEBUG = True
SECRET_KEY = 'yekterces'
SQLALCHEMY_DATABASE_URI = 'sqlite:///db/sql.db'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['MONGO_DBNAME'] = 'local'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/local'

app.register_blueprint(account_api)

mongo = PyMongo(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '127.0.0.1')

    app.run(port=port, host=host)

