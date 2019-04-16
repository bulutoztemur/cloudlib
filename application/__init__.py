from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os






app = Flask(__name__)
S_KEY = os.environ.get('SEC_KEY', None)
app.config['SECRET_KEY'] = S_KEY
DB_URL = os.environ.get('DATABASE_URL', None)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
Bootstrap(app)

from application import routes