import os
import secrets
from flask import Flask, render_template_string, render_template
from flask_security import Security, current_user, auth_required, hash_password, logout_user, \
    SQLAlchemySessionUserDatastore
from database import init_db, db_session
from models import *
from flask_babelex import Babel
from dotenv import load_dotenv
from datetime import date

# SETUP FLASK
# Create app and setup Babel communication
app = Flask(__name__)
app.config['DEBUG'] = True
babel = Babel(app)
# Monkeypatching Flask-babelex
babel.domain = 'flask_user'
babel.translation_directories = 'translations'
# SETUP FLASK_SECURITY

if not os.path.isfile('.env'):
    confFile = open(".env", 'w')
    confFile.write('SECRET_KEY=' + str(secrets.token_urlsafe()) + '\n')
    confFile.write('SECURITY_PASSWORD_SALT=' + str(secrets.SystemRandom().getrandbits(128)))
    confFile.close()

load_dotenv()

# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT")

app.config['SECURITY_REGISTERABLE'] = True
# app.config['SECURITY_CONFIRMABLE'] = True
# app.config['SECURITY_CONFIRM_EMAIL_WITHIN'] = '1 days'
app.config['SECURITY_POST_LOGIN_VIEW'] = '/form'
# app.config['SECURITY_RECOVERABLE'] = True
# app.config['SECURITY_RESET_PASSWORD_WITHIN'] = '1 days'

init_db()
# Linking flask-security with user and role table
user_datastore = SQLAlchemySessionUserDatastore(db_session, Users, Roles)
security = Security(app, user_datastore)


# Create a user to test with
@app.before_first_request
def create_user():
    if not user_datastore.find_user(email="test@me.com"):
        user_datastore.create_user(email="test@me.com", password=hash_password("password"))
    birthday_form = Forms(name='Festa Compleanno', dataCreation=date.today(),
                          description='Invitation for birthday party',
                          creator_id=1)
    birthday_q1 = Questions(text="What time do you prefer?")
    birthday_q1_details = OpenQuestions(id=birthday_q1.id)
    db_session.add_all([birthday_form, birthday_q1, birthday_q1_details])
    db_session.commit()


# HomePage
@app.route("/")
def home():
    return "Hello frome home!\n"


@app.route("/logout")
@auth_required()
def logout():
    logout_user()
    return 'Logout Done'


@app.route("/form")
@auth_required()
def form():
    r1 = db_session.query(Forms.name).where(Forms.creator == current_user)
    return r1.all()


if __name__ == '__main__':
    app.run()
