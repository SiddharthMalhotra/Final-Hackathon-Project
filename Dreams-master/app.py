from flask import *
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from pymongo import MongoClient
import database
from flask import jsonify
from decimal import Decimal
import math


import os
import sys

DEBUG = True
SECRET_KEY = 'yekterces'

app = Flask(__name__)
app.config.from_object(__name__)
database.mongo = MongoClient('localhost', 27017)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

from account_api import account_api
app.register_blueprint(account_api)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '127.0.0.1')

    app.run(port=port, host=host)

