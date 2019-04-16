from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os






app = Flask(__name__)
app.config['SECRET_KEY'] = '\x1f\xeb\xda\xbe\xbd1\xd8\xda\xcf\xc5\xa6e]vQ_k.\xe0\x82\x9a\xea\xe6\xc1'
DB_URL = os.environ.get('DATABASE_URL', None)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
Bootstrap(app)

from application import routes