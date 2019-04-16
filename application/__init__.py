from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = '\x1f\xeb\xda\xbe\xbd1\xd8\xda\xcf\xc5\xa6e]vQ_k.\xe0\x82\x9a\xea\xe6\xc1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ghxubndgrsqqbw:27815973445b0f3b9f42607322204077c5f9fc6408b19430c6240c79afacd769@ec2-54-246-92-116.eu-west-1.compute.amazonaws.com:5432/d5up03ss7quea6'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
Bootstrap(app)

from application import routes