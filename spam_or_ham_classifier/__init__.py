# from spam_or_ham_classifier.routes_and_forms.forms import RegistrationForm, LoginForm
# from spam_or_ham_classifier.web_database import engine, Base, session

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web_database/spam_or_ham_db'
db = SQLAlchemy(app)

# encrypted data (passwords)
bcrypt = Bcrypt(app)


login_manager = LoginManager(app)
# accesses to register user
login_manager.login_view = 'login_func'
# message font
login_manager.login_message_category = 'info'

