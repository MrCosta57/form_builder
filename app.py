import os
import secrets
from flask import Flask, render_template_string, render_template
from flask_security import Security, current_user, auth_required, hash_password, logout_user, \
    SQLAlchemySessionUserDatastore
from database import open_session,close_session, init_db
from models import User, Role
from flask_babelex import Babel
from dotenv import load_dotenv

# Load .env for security key
load_dotenv()

# SETUP FLASK
# Create app and setup Babel communication
app = Flask(__name__)
app.config['DEBUG'] = True
babel = Babel(app)
# Monkeypatching Flask-babelex
babel.domain = 'flask_user'
babel.translation_directories = 'translations'

# SETUP FLASK_SECURITY
# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT",
                                                      'ciao')

# SETUP DATABASE
db_session = open_session()

# Linking flask-security with user and role table
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)
close_session(db_session)


# Create a user to test with
@app.before_first_request
def create_user():
    session = open_session()
    init_db()
    if not user_datastore.find_user(email="test@me.com"):
        user_datastore.create_user(email="test@me.com", password=hash_password("password"))
    session.commit()
    close_session(session)


# Views
@app.route("/")
@auth_required()
def home():
    return render_template('index.html')


@app.route("/login.html")
@auth_required()
def login():
    return render_template('login.html')


@app.route("/logout")
@auth_required()
def logout():
    logout_user()
    return render_template_string('Logout Done')


if __name__ == '__main__':
    app.run()
