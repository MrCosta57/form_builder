import os
import secrets
from flask import Flask, render_template, redirect, url_for, send_from_directory, request
from flask_mail import Mail
from flask_security import Security, current_user, auth_required, logout_user, \
    SQLAlchemySessionUserDatastore
from flask_security.forms import ConfirmRegisterForm, Required
from flask_security.utils import hash_password
from wtforms import TextField, DateField

from form_function import *
from form_management_BP import form_management_BP
from database import init_db, db_session
from models import *
from flask_babelex import Babel
from dotenv import load_dotenv
from datetime import date, datetime

# SETUP FLASK
# Create app, setup Babel communication and Mail configuration, BluePrint Registration
app = Flask(__name__)
app.register_blueprint(form_management_BP)
init_db()

# LIST OF CONFIGS
app.config['DEBUG'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'Info.progbd.dblegends@gmail.com'
app.config['MAIL_PASSWORD'] = 'db_legends00'
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_CONFIRM_EMAIL_WITHIN'] = '1 days'
app.config['SECURITY_POST_LOGIN_VIEW'] = '/'
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_RESET_PASSWORD_WITHIN'] = '1 days'


# Generate a nice key using secrets.token_urlsafe()
if not os.path.isfile('.env'):
    confFile = open('.env', 'w')
    confFile.write('SECRET_KEY=' + str(secrets.token_urlsafe()) + '\n')
    # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
    # Generate a good salt using: secrets.SystemRandom().getrandbits(128)
    confFile.write('SECURITY_PASSWORD_SALT=' + str(secrets.SystemRandom().getrandbits(128)))
    confFile.close()

load_dotenv()

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SECURITY_PASSWORD_SALT'] = os.environ['SECURITY_PASSWORD_SALT']


# extends RegisterForm of flask
class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
    name = TextField('Nome', [Required()])
    surname = TextField('Cognome', [Required()])
    date = DateField('Data di nascita', format='%d-%m-%Y', default=date.today())
    username = TextField('Username', [Required()])


# Linking flask-security with user and role table
user_datastore = SQLAlchemySessionUserDatastore(db_session, Users, Roles)

# Init mail, babel e security
security = Security(app, user_datastore, confirm_register_form=ExtendedConfirmRegisterForm)
mail = Mail(app)
babel = Babel(app)

# Monkeypatching Flask-babelex
babel.domain = 'flask_user'
babel.translation_directories = 'translations'


# Populate database
@app.before_first_request
def init():
    if not user_datastore.find_user(email="admin@db.com"):
        create_roles()
        create_admin_user()
        populate_tags()
        init_base_question()
        template_party(1, "Party Form", "Invito per una festa")
        template_meets(1, "Meets Form", "Meeting")
        template_events(1, "Events Form", "Evento")
        template_contacts(1, "Form Informativo", "Informazioni personali")


def create_roles():
    user_datastore.create_role(name="Admin", description="App administrator")
    user_datastore.create_role(name="Standard User", description="Standard app user")


def create_admin_user():
    user_datastore.create_user(email="admin@db.com", password=hash_password("password"),
                               username="admin", name="Admin", surname="Admin", date=date.today(),
                               confirmed_at=datetime.now())
    db_session.commit()
    admin = db_session.query(Users).filter(Users.id == 1).first()
    role = db_session.query(Roles).filter(Roles.id == 1).first()
    user_datastore.add_role_to_user(admin, role)


# HomePage
@app.route("/")
def home():
    return render_template("index.html", user=current_user)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Logout
@app.route("/logout")
@auth_required()
def logout():
    logout_user()
    return redirect(url_for('home'))


# Visualize the user profile
@app.route("/profile", methods=['GET', 'POST'])
@auth_required()
def user_profile():
    if request.method == 'POST':
        # TODO: L'ADMIN NON PUO' CANCELLARE IL PROFILE
        id_user = current_user.id
        logout_user()
        db_session.query(Users).filter(Users.id == id_user).delete()
        db_session.commit()
        return redirect(url_for("home"))

    return render_template("profile.html", user=current_user)


@app.route("/profile/edit", methods=['GET', 'POST'])
@auth_required()
def edit_profile():
    if request.method == 'POST':
        req = request.form
        db_session.query(Users).filter(Users.id == current_user.id).update({"name": req.get("name"),
                                                                            "surname": req.get("surname"),
                                                                            "date": req.get("b_date"),
                                                                            "username": req.get("username")
                                                                            })
        db_session.commit()
        return redirect(url_for('user_profile'))

    return render_template("edit_profile.html", user=current_user)


# Run the app
if __name__ == '__main__':
    app.run()
