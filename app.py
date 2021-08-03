import os
import secrets
from flask import Flask, render_template, request, redirect, url_for
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
    return render_template("home_page.html", user=current_user)


@app.route("/logout")
@auth_required()
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/form")
@auth_required()
def form():
    user_query = db_session.query(Users).filter(Users.id == current_user.id).first()
    form = db_session.query(Forms).filter(Forms.creator_id == user_query.id)
    # Passo al template un oggetto di tipo Form
    return render_template("forms_list.html", user=user_query, forms=form)


@app.route("/form/form_create", methods=['GET', 'POST'])
def form_create():
    if request.method == "POST":
        req = request.form
        nome = req.get("name")
        descrizione = req.get("description")
        db_session.add(Forms(name=nome, dataCreation=date.today(),
                             description=descrizione,
                             creator_id=current_user.id))
        db_session.commit()
        return redirect(url_for('form'))

    return render_template("form_create.html", user=current_user)


@app.route("/form/<form_id>/add_question", methods=['GET', 'POST'])
def form_add_question(form_id):
    form = db_session.query(Forms).filter(Forms.id == form_id).first()
    if request.method == "POST":
        req = request.form
        if req.get("choose") == "si":
            id_q = req.get("question_choose")
            db_session.add(FormsQuestions(form_id=form_id, question_id=id_q))
            db_session.commit()
        else:
            tag = req.get("tag_choose")
            if tag == "nuovo":
                new_tag = req.get("tag_aggiunto")
                db_session.add(Tags(argument=new_tag))
                db_session.commit()
                tag = new_tag
            tipo_domanda = req.get("tipo_domanda")
            text_question = req.get("text_question")
            print(tag)
            id_t = (db_session.query(Tags.id).filter(Tags.argument == tag).first())[0]
            if tipo_domanda == "open":
                db_session.add(Questions(text=text_question))
                db_session.commit()
                id_q = (db_session.query(Questions.id).filter(Questions.text == text_question).first())[0]
                db_session.add(OpenQuestions(id=id_q))
                db_session.commit()
                db_session.add(TagsQuestions(tag_id=id_t, question_id=id_q))
                db_session.add(FormsQuestions(form_id=form_id, question_id=id_q))
            elif tipo_domanda == "single":
                db_session.add(Questions(text=text_question))
                db_session.commit()
                id_q = (db_session.query(Questions.id).filter(Questions.text == text_question).first())[0]
                db_session.add(SingleQuestions(id=id_q))
                db_session.commit()
                db_session.add(TagsQuestions(tag_id=id_t, question_id=id_q))

                number = req.get("number_answers")

                for i in range(1, int(number)+1):
                    cont = req.get(str(i))
                    db_session.add(PossibleAnswersS(idPosAnswS=id_q, content=cont))
                db_session.add(FormsQuestions(form_id=form_id, question_id=id_q))
            elif tipo_domanda == "multiple_choice":
                db_session.add(Questions(text=text_question))
                db_session.commit()
                id_q = (db_session.query(Questions.id).filter(Questions.text == text_question).first())[0]
                db_session.add(MultipleChoiceQuestions(id=id_q))
                db_session.commit()
                db_session.add(TagsQuestions(tag_id=id_t, question_id=id_q))

                number = req.get("number_answers")

                for i in range(1, int(number)+1):
                    cont = req.get(str(i))
                    db_session.add(PossibleAnswersM(idPosAnswM=id_q, content=cont))
                db_session.add(FormsQuestions(form_id=form_id, question_id=id_q))
            db_session.commit()
        return redirect(url_for('form_edit', form_id=form_id))
    tags = db_session.query(Tags)
    questions = db_session.query(Questions)
    return render_template("question_add.html", form=form, tags=tags, questions=questions)


@app.route("/form/<form_id>/edit")
@auth_required()
def form_edit(form_id):
    form = db_session.query(Forms).filter(Forms.id == form_id).first()
    return render_template("form_edit.html", user=current_user, questions=form.questions, form=form)


@app.route("/form/<form_id>/viewform", methods=['GET', 'POST'])
@auth_required()
def form_view(form_id):
    form = db_session.query(Forms).filter(Forms.id == form_id).first()
    if request.method == "POST":
        req = request.form
        for q in form.questions:
            if not q.multiple_choice:
                text = [req.get(str(q.id))]
            else:
                text = req.getlist(str(q.id))
            db_session.add(Answers(form_id=form_id, question_id=q.id, user_id=current_user.id))
            db_session.commit()
            ans_id = db_session.query(Answers.id).filter(Answers.form_id == form_id).filter(
                Answers.question_id == q.id).filter(Answers.user_id == current_user.id).first()
            if text:
                for t in text:
                    db_session.add(SeqAnswers(id=ans_id[0], content=t))
            else:
                db_session.add(SeqAnswers(id=ans_id[0], content=''))
            db_session.commit()
        return redirect(url_for('home'))

    if True: #TODO: current_user.id != form.creator_id:
        return render_template("form.html", user=current_user, questions=form.questions, form=form)
    else:
        return render_template("form_edit.html", user=current_user, questions=form.questions, form=form)


@app.route("/form/<form_id>/answers")
@auth_required()
def form_answers(form_id):
    answers = db_session.query(Answers).filter(Answers.form_id == form_id)
    total_answers = db_session.query(Answers.user_id).filter(Answers.form_id == form_id).group_by(Answers.user_id).count()
    form = db_session.query(Forms).filter(Forms.id == form_id).first()
    return render_template("form_answers.html", user=current_user, answers=answers, form=form, total_answers=total_answers)


@app.route("/profile")
@auth_required()
def user_profile():
    # pagina che mostra le info utente, da vedere se crearne un'altra per la modifica delle info
    # query che ricava le info dal current user e le passa alla pagina profile.html
    return render_template("profile.html", user=current_user)


# @app.route("/edit_profile")
# @auth_required()
# def Edit(request):
#    drinker = request.user.get_profile()
#    context = {'drinker': drinker}
#    return render_to_response('form_edit.html', context, context_instance=RequestContext(request))


if __name__ == '__main__':
    app.run()
