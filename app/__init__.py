from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user
import pymysql
import os
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://rawlings:1234@localhost:8889/test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.fatcow.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dev@rawlings.site'
app.config['MAIL_PASSWORD'] = 'Test1Test'
app.config['MAIL_DEBUG'] = False
app.config['MAIL_SUPPRESS_SEND'] = True
app.config['TESTING'] = False


db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app import routes