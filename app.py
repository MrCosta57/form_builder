import os
import secrets
from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask_mail import Mail
from flask_security import Security, current_user, auth_required, logout_user, \
    SQLAlchemySessionUserDatastore
from flask_security.forms import ConfirmRegisterForm, Required
from flask_security.utils import hash_password
from wtforms import TextField, DateField

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


class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
    name = TextField('Nome', [Required()])
    surname = TextField('Cognome', [Required()])
    date = DateField('Data di nascita', format='%Y-%m-%d', default=datetime.now())
    username = TextField('Username', [Required()])


# Linking flask-security with user and role table
user_datastore = SQLAlchemySessionUserDatastore(db_session, Users, Roles)

security = Security(app, user_datastore, confirm_register_form=ExtendedConfirmRegisterForm)
mail = Mail(app)
babel = Babel(app)

# Monkeypatching Flask-babelex
babel.domain = 'flask_user'
babel.translation_directories = 'translations'


@app.before_first_request
def init():
    if not user_datastore.find_user(email="admin@db.com"):
        create_admin_user()
        populate_tags()
        init_base_question()
        template_party()
        template_meets()
        template_events()
        template_contacts()


def create_admin_user():
    user_datastore.create_user(email="admin@db.com", password=hash_password("password"),
                               username="admin", name="Admin", surname="Admin", date=datetime.now(),
                               confirmed_at=datetime.now())
    db_session.commit()


def populate_tags():
    db_session.add_all([Tags(argument="Informazioni personali"),
                        Tags(argument="Organizzazione"),
                        Tags(argument="Altro"),
                        Tags(argument="Scuola"),
                        Tags(argument="Lavoro"),
                        Tags(argument="Animali"),
                        Tags(argument="Scienza"),
                        Tags(argument="Viaggio"),
                        Tags(argument="Ambiente"),
                        Tags(argument="Sondaggi")])
    db_session.commit()


def init_base_question():
    db_session.add_all([Questions(text="Nome"),
                        Questions(text="Cognome"),
                        Questions(text="Data Nascita"),
                        Questions(text="Età"),
                        Questions(text="Fascia d'età"),
                        Questions(text="Lavoro"),
                        Questions(text="Sesso"),
                        Questions(text="Mail"),
                        Questions(text="Paese di residenza"),
                        Questions(text="Via residenza"),
                        Questions(text="Inserisci l'orario che preferisci"),
                        Questions(text="Inserisci una data che preferisci"),
                        Questions(text="In quanti parteciperete?"),
                        Questions(text="Inserisci il giorno che preferisci"),
                        Questions(text="Scegli i giorni della settimana che preferisci"),
                        Questions(text="parteciperai all'evento?"),
                        Questions(text="Inserisci un breve commento"),
                        Questions(text="Valuta questo sondaggio"),
                        Questions(text="Come hai conosciuto questo evento?"),
                        Questions(text="Hai intolleranze alimentari, se si quali?"),
                        Questions(text="Che corsi hai seguito? "),
                        Questions(text="che materie studi?"),
                        Questions(text="Fai la raccolta differenziata?"),
                        Questions(text="Quali stati hai visitato?"),
                        Questions(text="Possiedi animali?"),
                        Questions(text="Animale preferito")])
    db_session.commit()

    db_session.add_all([OpenQuestions(id=1),
                        OpenQuestions(id=2),
                        OpenQuestions(id=3),
                        OpenQuestions(id=4),
                        SingleQuestions(idS=5),
                        OpenQuestions(id=6),
                        SingleQuestions(idS=7),
                        OpenQuestions(id=8),
                        OpenQuestions(id=9),
                        OpenQuestions(id=10),
                        OpenQuestions(id=11),
                        OpenQuestions(id=12),
                        OpenQuestions(id=13),
                        OpenQuestions(id=14),
                        MultipleChoiceQuestions(id=15),
                        SingleQuestions(idS=16),
                        OpenQuestions(id=17),
                        SingleQuestions(idS=18),
                        OpenQuestions(id=19),
                        OpenQuestions(id=20),
                        OpenQuestions(id=21),
                        OpenQuestions(id=22),
                        SingleQuestions(idS=23),
                        OpenQuestions(id=24),
                        OpenQuestions(id=25),
                        OpenQuestions(id=26),

                        TagsQuestions(tag_id=1, question_id=1),
                        TagsQuestions(tag_id=1, question_id=2),
                        TagsQuestions(tag_id=1, question_id=3),
                        TagsQuestions(tag_id=1, question_id=4),
                        TagsQuestions(tag_id=1, question_id=5),
                        TagsQuestions(tag_id=1, question_id=6),
                        TagsQuestions(tag_id=5, question_id=6),
                        TagsQuestions(tag_id=1, question_id=7),
                        TagsQuestions(tag_id=1, question_id=8),
                        TagsQuestions(tag_id=1, question_id=9),
                        TagsQuestions(tag_id=1, question_id=10),
                        TagsQuestions(tag_id=2, question_id=11),
                        TagsQuestions(tag_id=2, question_id=12),
                        TagsQuestions(tag_id=2, question_id=13),
                        TagsQuestions(tag_id=2, question_id=14),
                        TagsQuestions(tag_id=2, question_id=15),
                        TagsQuestions(tag_id=3, question_id=16),
                        TagsQuestions(tag_id=3, question_id=17),
                        TagsQuestions(tag_id=3, question_id=18),
                        TagsQuestions(tag_id=10, question_id=19),
                        TagsQuestions(tag_id=2, question_id=20),
                        TagsQuestions(tag_id=4, question_id=21),
                        TagsQuestions(tag_id=4, question_id=22),
                        TagsQuestions(tag_id=9, question_id=23),
                        TagsQuestions(tag_id=8, question_id=24),
                        TagsQuestions(tag_id=6, question_id=25),
                        TagsQuestions(tag_id=1, question_id=25),
                        TagsQuestions(tag_id=6, question_id=26)])
    db_session.commit()

    db_session.add_all([PossibleAnswersS(idPosAnswS=5, content="0-17"),
                        PossibleAnswersS(idPosAnswS=5, content="18-21"),
                        PossibleAnswersS(idPosAnswS=5, content="22-39"),
                        PossibleAnswersS(idPosAnswS=5, content="40-69"),
                        PossibleAnswersS(idPosAnswS=5, content="70+"),
                        PossibleAnswersS(idPosAnswS=7, content="M"),
                        PossibleAnswersS(idPosAnswS=7, content="F"),
                        PossibleAnswersS(idPosAnswS=16, content="Si"),
                        PossibleAnswersS(idPosAnswS=16, content="No"),
                        PossibleAnswersS(idPosAnswS=18, content="1"),
                        PossibleAnswersS(idPosAnswS=18, content="2"),
                        PossibleAnswersS(idPosAnswS=18, content="3"),
                        PossibleAnswersS(idPosAnswS=18, content="4"),
                        PossibleAnswersS(idPosAnswS=18, content="5"),
                        PossibleAnswersS(idPosAnswS=23, content="Si"),
                        PossibleAnswersS(idPosAnswS=23, content="No"),
                        PossibleAnswersM(idPosAnswM=15, content="lunedì"),
                        PossibleAnswersM(idPosAnswM=15, content="martedì"),
                        PossibleAnswersM(idPosAnswM=15, content="mercoledì"),
                        PossibleAnswersM(idPosAnswM=15, content="giovedì"),
                        PossibleAnswersM(idPosAnswM=15, content="venerdì"),
                        PossibleAnswersM(idPosAnswM=15, content="sabato"),
                        PossibleAnswersM(idPosAnswM=15, content="domenica")])
    db_session.commit()


def template_party():
    db_session.add(Forms(name='Party Form', dataCreation=date.today(),
                         description='Invito per una festa',
                         creator_id=1))
    db_session.commit()

    db_session.add_all([FormsQuestions(form_id=1, question_id=1),
                        FormsQuestions(form_id=1, question_id=2),
                        FormsQuestions(form_id=1, question_id=11),
                        FormsQuestions(form_id=1, question_id=15),
                        FormsQuestions(form_id=1, question_id=13),
                        FormsQuestions(form_id=1, question_id=16)])
    db_session.commit()


def template_meets():
    db_session.add(Forms(name='Meets Form', dataCreation=date.today(),
                         description='Meeting',
                         creator_id=1))
    db_session.commit()

    db_session.add_all([FormsQuestions(form_id=2, question_id=1),
                        FormsQuestions(form_id=2, question_id=2),
                        FormsQuestions(form_id=2, question_id=4),
                        FormsQuestions(form_id=2, question_id=7),
                        FormsQuestions(form_id=2, question_id=8),
                        FormsQuestions(form_id=2, question_id=13),
                        FormsQuestions(form_id=2, question_id=20)])
    db_session.commit()


def template_events():
    db_session.add(Forms(name='Events Form', dataCreation=date.today(),
                         description='Evento',
                         creator_id=1))
    db_session.commit()

    db_session.add_all([FormsQuestions(form_id=3, question_id=1),
                        FormsQuestions(form_id=3, question_id=2),
                        FormsQuestions(form_id=3, question_id=3),
                        FormsQuestions(form_id=3, question_id=5),
                        FormsQuestions(form_id=3, question_id=16),
                        FormsQuestions(form_id=3, question_id=20)])
    db_session.commit()


def template_contacts():
    db_session.add(Forms(name='Form Informativo', dataCreation=date.today(),
                         description='Informazioni personali',
                         creator_id=1))
    db_session.commit()

    db_session.add_all([FormsQuestions(form_id=4, question_id=1),
                        FormsQuestions(form_id=4, question_id=2),
                        FormsQuestions(form_id=4, question_id=5),
                        FormsQuestions(form_id=4, question_id=6),
                        FormsQuestions(form_id=4, question_id=7),
                        FormsQuestions(form_id=4, question_id=8),
                        FormsQuestions(form_id=4, question_id=9),
                        FormsQuestions(form_id=4, question_id=10)])
    db_session.commit()


# HomePage
@app.route("/")
def home():
    return render_template("index.html", user=current_user)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/logout")
@auth_required()
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/profile")
@auth_required()
def user_profile():
    # pagina che mostra le info utente, da vedere se crearne un'altra per la modifica delle info
    # query che ricava le info dal current user e le passa alla pagina profile.html
    return render_template("profile.html", user=current_user)


if __name__ == '__main__':
    app.run()
