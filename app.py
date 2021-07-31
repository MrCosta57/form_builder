import os
import secrets
from flask import Flask, render_template
from flask_mail import Mail
from flask_security import Security, current_user, auth_required, logout_user, \
    SQLAlchemySessionUserDatastore
from flask_security.forms import ConfirmRegisterForm, Required
from flask_security.utils import hash_password
from wtforms import TextField, DateField

from database import init_db, db_session
from models import *
from flask_babelex import Babel
from dotenv import load_dotenv
from datetime import date, datetime

# SETUP FLASK
# Create app, setup Babel communication and Mail configuration

app = Flask(__name__)
init_db()

# ELENCO CONFIG
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
# app.config['SECURITY_CONFIRM_EMAIL_WITHIN'] = '1 days'
app.config['SECURITY_POST_LOGIN_VIEW'] = '/form'
# app.config['SECURITY_RECOVERABLE'] = True
# app.config['SECURITY_RESET_PASSWORD_WITHIN'] = '1 days'
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
    user_datastore.create_user(id=0, email="admin@db.com", password=hash_password("password"),
                               username="admin", name="Admin", surname="Admin", date=datetime.now(),
                               confirmed_at=datetime.now())
    db_session.commit()


def populate_tags():
    db_session.add_all([Tags(id=0, argument="Informazioni personali"),
                        Tags(id=1, argument="Organizzazione"),
                        Tags(id=2, argument="Altro"),
                        Tags(id=3, argument="Scuola"),
                        Tags(id=4, argument="Lavoro"),
                        Tags(id=5, argument="Animali"),
                        Tags(id=6, argument="Scienza"),
                        Tags(id=7, argument="Viaggio"),
                        Tags(id=8, argument="Ambiente"),
                        Tags(id=9, argument="Sondaggi")])
    db_session.commit()


def init_base_question():
    db_session.add_all([Questions(id=0, text="Nome"),
                        Questions(id=1, text="Cognome"),
                        Questions(id=2, text="Data Nascita"),
                        Questions(id=3, text="Età"),
                        Questions(id=4, text="Fascia d'età"),
                        Questions(id=5, text="Lavoro"),
                        Questions(id=6, text="Sesso"),
                        Questions(id=7, text="Mail"),
                        Questions(id=8, text="Paese di residenza"),
                        Questions(id=9, text="Via residenza"),
                        Questions(id=10, text="Inserisci l'orario che preferisci"),
                        Questions(id=11, text="Inserisci una data che preferisci"),
                        Questions(id=12, text="In quanti parteciperete?"),
                        Questions(id=13, text="Inserisci il giorno che preferisci"),
                        Questions(id=14, text="Scegli due giorni della settimana che preferisci"),
                        Questions(id=15, text="parteciperai all'evento?"),
                        Questions(id=16, text="Inserisci un breve commento"),
                        Questions(id=17, text="Valuta questo sondaggio"),
                        Questions(id=18, text="Come hai conosciuto questo evento?"),
                        Questions(id=19, text="Hai intolleranze alimentari, se si quali?"),
                        Questions(id=20, text="Che corsi hai seguito? "),
                        Questions(id=21, text="che materie studi?"),
                        Questions(id=22, text="Fai la raccolta differenziata?"),
                        Questions(id=23, text="Quali stati hai visitato?"),
                        Questions(id=24, text="Possiedi animali?"),
                        Questions(id=25, text="Animale preferito")])
    db_session.commit()

    db_session.add_all([OpenQuestions(id=0),
                        OpenQuestions(id=1),
                        OpenQuestions(id=2),
                        OpenQuestions(id=3),
                        SingleQuestions(idS=4),
                        OpenQuestions(id=5),
                        SingleQuestions(idS=6),
                        OpenQuestions(id=7),
                        OpenQuestions(id=8),
                        OpenQuestions(id=9),
                        OpenQuestions(id=10),
                        OpenQuestions(id=11),
                        OpenQuestions(id=12),
                        OpenQuestions(id=13),
                        MultipleChoiceQuestions(id=14),
                        SingleQuestions(idS=15),
                        OpenQuestions(id=16),
                        SingleQuestions(idS=17),
                        OpenQuestions(id=18),
                        OpenQuestions(id=19),
                        OpenQuestions(id=20),
                        OpenQuestions(id=21),
                        SingleQuestions(idS=22),
                        OpenQuestions(id=23),
                        OpenQuestions(id=24),
                        OpenQuestions(id=25),

                        TagsQuestions(tag_id=0, question_id=0),
                        TagsQuestions(tag_id=0, question_id=1),
                        TagsQuestions(tag_id=0, question_id=2),
                        TagsQuestions(tag_id=0, question_id=3),
                        TagsQuestions(tag_id=0, question_id=4),
                        TagsQuestions(tag_id=0, question_id=5),
                        TagsQuestions(tag_id=4, question_id=5),
                        TagsQuestions(tag_id=0, question_id=6),
                        TagsQuestions(tag_id=0, question_id=7),
                        TagsQuestions(tag_id=0, question_id=8),
                        TagsQuestions(tag_id=0, question_id=9),
                        TagsQuestions(tag_id=1, question_id=10),
                        TagsQuestions(tag_id=1, question_id=11),
                        TagsQuestions(tag_id=1, question_id=12),
                        TagsQuestions(tag_id=1, question_id=13),
                        TagsQuestions(tag_id=1, question_id=14),
                        TagsQuestions(tag_id=2, question_id=15),
                        TagsQuestions(tag_id=2, question_id=16),
                        TagsQuestions(tag_id=2, question_id=17),
                        TagsQuestions(tag_id=9, question_id=18),
                        TagsQuestions(tag_id=1, question_id=19),
                        TagsQuestions(tag_id=3, question_id=20),
                        TagsQuestions(tag_id=3, question_id=21),
                        TagsQuestions(tag_id=8, question_id=22),
                        TagsQuestions(tag_id=7, question_id=23),
                        TagsQuestions(tag_id=5, question_id=24),
                        TagsQuestions(tag_id=0, question_id=24),
                        TagsQuestions(tag_id=5, question_id=25)])
    db_session.commit()

    db_session.add_all([PossibleAnswersS(idPosAnswS=4, content="0-17"),
                        PossibleAnswersS(idPosAnswS=4, content="18-21"),
                        PossibleAnswersS(idPosAnswS=4, content="22-39"),
                        PossibleAnswersS(idPosAnswS=4, content="40-69"),
                        PossibleAnswersS(idPosAnswS=4, content="70+"),
                        PossibleAnswersS(idPosAnswS=6, content="M"),
                        PossibleAnswersS(idPosAnswS=6, content="F"),
                        PossibleAnswersS(idPosAnswS=15, content="Si"),
                        PossibleAnswersS(idPosAnswS=15, content="No"),
                        PossibleAnswersS(idPosAnswS=17, content="1"),
                        PossibleAnswersS(idPosAnswS=17, content="2"),
                        PossibleAnswersS(idPosAnswS=17, content="3"),
                        PossibleAnswersS(idPosAnswS=17, content="4"),
                        PossibleAnswersS(idPosAnswS=17, content="5"),
                        PossibleAnswersS(idPosAnswS=22, content="Si"),
                        PossibleAnswersS(idPosAnswS=22, content="No"),
                        PossibleAnswersM(idPosAnswM=14, content="lunedì"),
                        PossibleAnswersM(idPosAnswM=14, content="martedì"),
                        PossibleAnswersM(idPosAnswM=14, content="mercoledì"),
                        PossibleAnswersM(idPosAnswM=14, content="giovedì"),
                        PossibleAnswersM(idPosAnswM=14, content="venerdì"),
                        PossibleAnswersM(idPosAnswM=14, content="sabato"),
                        PossibleAnswersM(idPosAnswM=14, content="domenica")])
    db_session.commit()


def template_party():
    db_session.add(Forms(id=0, name='Party Form', dataCreation=date.today(),
                         description='Invito per una festa',
                         creator_id=0))
    db_session.commit()

    db_session.add_all([FormsQuestions(form_id=0, question_id=0),
                        FormsQuestions(form_id=0, question_id=1),
                        FormsQuestions(form_id=0, question_id=10),
                        FormsQuestions(form_id=0, question_id=14),
                        FormsQuestions(form_id=0, question_id=12),
                        FormsQuestions(form_id=0, question_id=15)])
    db_session.commit()


def template_meets():
    db_session.add(Forms(id=1, name='Meets Form', dataCreation=date.today(),
                         description='Meeting',
                         creator_id=0))
    db_session.commit()

    db_session.add_all([FormsQuestions(form_id=1, question_id=0),
                        FormsQuestions(form_id=1, question_id=1),
                        FormsQuestions(form_id=1, question_id=3),
                        FormsQuestions(form_id=1, question_id=6),
                        FormsQuestions(form_id=1, question_id=7),
                        FormsQuestions(form_id=1, question_id=12),
                        FormsQuestions(form_id=1, question_id=19)])
    db_session.commit()


def template_events():
    db_session.add(Forms(id=2, name='Events Form', dataCreation=date.today(),
                         description='Evento',
                         creator_id=0))
    db_session.commit()

    db_session.add_all([FormsQuestions(form_id=2, question_id=0),
                        FormsQuestions(form_id=2, question_id=1),
                        FormsQuestions(form_id=2, question_id=2),
                        FormsQuestions(form_id=2, question_id=4),
                        FormsQuestions(form_id=2, question_id=15),
                        FormsQuestions(form_id=2, question_id=19)])
    db_session.commit()


def template_contacts():
    db_session.add(Forms(id=3, name='Form Informativo', dataCreation=date.today(),
                         description='Informazioni personali',
                         creator_id=0))
    db_session.commit()

    db_session.add_all([FormsQuestions(form_id=3, question_id=0),
                        FormsQuestions(form_id=3, question_id=1),
                        FormsQuestions(form_id=3, question_id=4),
                        FormsQuestions(form_id=3, question_id=5),
                        FormsQuestions(form_id=3, question_id=6),
                        FormsQuestions(form_id=3, question_id=7),
                        FormsQuestions(form_id=3, question_id=8),
                        FormsQuestions(form_id=3, question_id=9)])
    db_session.commit()


# HomePage
@app.route("/")
def home():
    return render_template("home_page.html", user=current_user)


@app.route("/logout")
@auth_required()
def logout():
    logout_user()
    return 'Logout Done'


@app.route("/form")
@auth_required()
def form():
    user_query = db_session.query(Users).filter(Users.id == current_user.id).first()
    form = db_session.query(Forms).filter(Forms.creator_id == user_query.id)
    # Passo al template un oggetto di tipo Form
    return render_template("forms_list.html", user=user_query, forms=form)


@app.route("/form/<form_id>/edit")
@auth_required()
def form_edit(form_id):
    # query con form id: ...
    # Passo al template un oggetto di tipo Form, poi nel template farò le query in caso
    return "Ciao da form_id edit"


@app.route("/form/<form_id>/viewform")
@auth_required()
def form_view(form_id):
    # query con form id: ...
    # Passo al template un oggetto di tipo Form, poi nel template farò le query in caso
    form = db_session.query(Forms).filter(Forms.id == form_id).first()
    return render_template("form.html", user=current_user, questions=form.questions, form=form)


@app.route("/profile")
@auth_required()
def user_profile():
    # pagina che mostra le info utente, da vedere se crearne un'altra per la modifica delle info
    # query che ricava le info dal current user e le passa alla pagina profile.html
    user_query = db_session.query(Users).filter(Users.id == current_user.id).first()
    # TODO: da vedere, es filter_by(current_user=username)
    return render_template("profile.html", user=user_query)


#   Stampare lista:
#   {% for u in user %}
#   <li>{{u.name}}</li>
#   {% endfor %}

@app.route("/edit_profile")
@auth_required()
def Edit(request):
    drinker = request.user.get_profile()
    context = {'drinker': drinker}
    return render_to_response('edit.html', context, context_instance=RequestContext(request))


if __name__ == '__main__':
    app.run()
