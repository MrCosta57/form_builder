from datetime import date
from flask import render_template, request, redirect, url_for, Blueprint
from flask_security import current_user, auth_required
from database import db_session
from models import *

form_management_BP = Blueprint('form_management_BP', __name__, template_folder='templates/form', url_prefix='/form')


def template_party(id_user, name, description):
    db_session.add(Forms(name=name, dataCreation=date.today(),
                         description=description,
                         creator_id=id_user))
    db_session.commit()

    id_f = db_session.query(Forms.id).filter(Forms.name == name).filter(Forms.creator_id == id_user).first()[0]

    db_session.add_all([FormsQuestions(form_id=id_f, question_id=1),
                        FormsQuestions(form_id=id_f, question_id=2),
                        FormsQuestions(form_id=id_f, question_id=11),
                        FormsQuestions(form_id=id_f, question_id=15),
                        FormsQuestions(form_id=id_f, question_id=13),
                        FormsQuestions(form_id=id_f, question_id=16)])
    db_session.commit()


def template_meets(id_user, name, description):
    db_session.add(Forms(name=name, dataCreation=date.today(),
                         description=description,
                         creator_id=id_user))
    db_session.commit()

    id_f = db_session.query(Forms.id).filter(Forms.name == name).filter(Forms.creator_id == id_user).first()[0]

    db_session.add_all([FormsQuestions(form_id=id_f, question_id=1),
                        FormsQuestions(form_id=id_f, question_id=2),
                        FormsQuestions(form_id=id_f, question_id=4),
                        FormsQuestions(form_id=id_f, question_id=7),
                        FormsQuestions(form_id=id_f, question_id=8),
                        FormsQuestions(form_id=id_f, question_id=13),
                        FormsQuestions(form_id=id_f, question_id=20)])
    db_session.commit()


def template_events(id_user, name, description):
    db_session.add(Forms(name=name, dataCreation=date.today(),
                         description=description,
                         creator_id=id_user))
    db_session.commit()

    id_f = db_session.query(Forms.id).filter(Forms.name == name).filter(Forms.creator_id == id_user).first()[0]

    db_session.add_all([FormsQuestions(form_id=id_f, question_id=1),
                        FormsQuestions(form_id=id_f, question_id=2),
                        FormsQuestions(form_id=id_f, question_id=3),
                        FormsQuestions(form_id=id_f, question_id=5),
                        FormsQuestions(form_id=id_f, question_id=16),
                        FormsQuestions(form_id=id_f, question_id=20)])
    db_session.commit()


def template_contacts(id_user, name, description):
    db_session.add(Forms(name=name, dataCreation=date.today(),
                         description=description,
                         creator_id=id_user))
    db_session.commit()

    id_f = \
    db_session.query(Forms.id).filter(Forms.name == name).filter(Forms.creator_id == id_user).first()[0]

    db_session.add_all([FormsQuestions(form_id=id_f, question_id=1),
                        FormsQuestions(form_id=id_f, question_id=2),
                        FormsQuestions(form_id=id_f, question_id=5),
                        FormsQuestions(form_id=id_f, question_id=6),
                        FormsQuestions(form_id=id_f, question_id=7),
                        FormsQuestions(form_id=id_f, question_id=8),
                        FormsQuestions(form_id=id_f, question_id=9),
                        FormsQuestions(form_id=id_f, question_id=10)])
    db_session.commit()


# Endpoint for the list of forms of the current user
@form_management_BP.route("/")
@auth_required()
def form():
    user_query = db_session.query(Users).filter(Users.id == current_user.id).first()
    form = db_session.query(Forms).filter(Forms.creator_id == user_query.id)
    return render_template("forms_list.html", user=user_query, forms=form)


# Create a form
@form_management_BP.route("/form_create", methods=['GET', 'POST'])
def form_create():
    if request.method == "POST":
        req = request.form
        # TODO: controllare che non esiste un form dello stesso utente con lo stesso nome
        choose = req.get("choose")
        nome = req.get("name")
        exist_form = db_session.query(Forms).filter(Forms.name == nome).filter(
            Forms.creator_id == current_user.id).first()
        if exist_form:
            return render_template("error.html", message="Hai già creato un form con questo nome")
        descrizione = req.get("description")
        if choose == "si":
            template = req.get("template")
            if template == "party":
                template_party(current_user.id, nome, descrizione)
            if template == "events":
                template_events(current_user.id, nome, descrizione)
            if template == "info":
                template_contacts(current_user.id, nome, descrizione)
            if template == "meeting":
                template_meets(current_user.id, nome, descrizione)

        else:
            db_session.add(Forms(name=nome, dataCreation=date.today(),
                                 description=descrizione,
                                 creator_id=current_user.id))
        db_session.commit()
        return redirect(url_for('form_management_BP.form'))
    forms = db_session.query(Forms)
    return render_template("form_create.html", user=current_user, forms=forms)


# Add a question to a specific form
@form_management_BP.route("/<form_id>/add_question", methods=['GET', 'POST'])
def form_add_question(form_id):
    form = db_session.query(Forms).filter(Forms.id == form_id).first()
    if request.method == "POST":
        req = request.form
        # Question already exists
        if req.get("choose") == "si":
            id_q = req.get("question_choose")
            db_session.add(FormsQuestions(form_id=form_id, question_id=id_q))
            db_session.commit()
        # new Question
        else:
            tag = req.get("tag_choose")
            # new Tag
            if tag == "nuovo":
                new_tag = req.get("tag_aggiunto")
                # add the tag to the database
                db_session.add(Tags(argument=new_tag))
                db_session.commit()
                tag = new_tag
            tipo_domanda = req.get("tipo_domanda")
            text_question = req.get("text_question")
            id_t = (db_session.query(Tags.id).filter(Tags.argument == tag).first())[0]
            # Type of the question
            if tipo_domanda == "open":
                # add the new question
                db_session.add(Questions(text=text_question))
                db_session.commit()
                id_q = (db_session.query(Questions.id).filter(Questions.text == text_question).first())[0]
                db_session.add(OpenQuestions(id=id_q))
                db_session.commit()
                # link the question with tag and form
                db_session.add(TagsQuestions(tag_id=id_t, question_id=id_q))
                db_session.add(FormsQuestions(form_id=form_id, question_id=id_q))
            elif tipo_domanda == "single":
                # add the new question
                db_session.add(Questions(text=text_question))
                db_session.commit()
                id_q = (db_session.query(Questions.id).filter(Questions.text == text_question).first())[0]
                db_session.add(SingleQuestions(id=id_q))
                db_session.commit()
                db_session.add(TagsQuestions(tag_id=id_t, question_id=id_q))
                # add the possibile answers
                number = req.get("number_answers")

                for i in range(1, int(number) + 1):
                    cont = req.get(str(i))
                    db_session.add(PossibleAnswersS(idPosAnswS=id_q, content=cont))
                # link the question with form
                db_session.add(FormsQuestions(form_id=form_id, question_id=id_q))
            elif tipo_domanda == "multiple_choice":
                # add the new question
                db_session.add(Questions(text=text_question))
                db_session.commit()
                id_q = (db_session.query(Questions.id).filter(Questions.text == text_question).first())[0]
                db_session.add(MultipleChoiceQuestions(id=id_q))
                db_session.commit()
                db_session.add(TagsQuestions(tag_id=id_t, question_id=id_q))
                # add the possibile answers
                number = req.get("number_answers")

                for i in range(1, int(number) + 1):
                    cont = req.get(str(i))
                    db_session.add(PossibleAnswersM(idPosAnswM=id_q, content=cont))
                # link the question with form
                db_session.add(FormsQuestions(form_id=form_id, question_id=id_q))
            db_session.commit()
        return redirect(url_for('form_management_BP.form_edit', form_id=form_id))

    tags = db_session.query(Tags)
    questions = db_session.query(Questions)
    return render_template("question_add.html", form=form, tags=tags, questions=questions)


# Editing a specific form
@form_management_BP.route("/<form_id>/edit")
@auth_required()
def form_edit(form_id):
    form = db_session.query(Forms).filter(Forms.id == form_id).first()
    return render_template("form_edit.html", user=current_user, questions=form.questions, form=form)


@form_management_BP.route("/<form_id>/<question_id>", methods=['GET', 'POST'])
def form_edit_question(form_id, question_id):
    form = db_session.query(Forms).filter(Forms.id == form_id).first()
    if request.method == "POST":
        req = request.form
        # Question already exists
        if req.get("choose") == "si":
            id_q = req.get("question_choose")
            db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id).filter(
                FormsQuestions.question_id == question_id) \
                .update({FormsQuestions.question_id: id_q}, synchronize_session=False)
            db_session.commit()
        # new Question
        else:
            tag = req.get("tag_choose")
            # new Tag
            if tag == "nuovo":
                new_tag = req.get("tag_aggiunto")
                # add the tag to the database
                db_session.add(Tags(argument=new_tag))
                db_session.commit()
                tag = new_tag
            tipo_domanda = req.get("tipo_domanda")
            text_question = req.get("text_question")
            id_t = (db_session.query(Tags.id).filter(Tags.argument == tag).first())[0]
            # Type of the question
            if tipo_domanda == "open":
                # add the new question
                db_session.add(Questions(text=text_question))
                db_session.commit()
                id_q = (db_session.query(Questions.id).filter(Questions.text == text_question).first())[0]
                db_session.add(OpenQuestions(id=id_q))
                db_session.commit()
                # link the question with tag and form
                db_session.add(TagsQuestions(tag_id=id_t, question_id=id_q))
                db_session.query(FormsQuestions).filter(form_id=form_id).filter(question_id=question_id) \
                    .update({FormsQuestions.question_id: id_q}, synchronize_session=False)
            elif tipo_domanda == "single":
                # add the new question
                db_session.add(Questions(text=text_question))
                db_session.commit()
                id_q = (db_session.query(Questions.id).filter(Questions.text == text_question).first())[0]
                db_session.add(SingleQuestions(id=id_q))
                db_session.commit()
                db_session.add(TagsQuestions(tag_id=id_t, question_id=id_q))
                # add the possibile answers
                number = req.get("number_answers")

                for i in range(1, int(number) + 1):
                    cont = req.get(str(i))
                    db_session.add(PossibleAnswersS(idPosAnswS=id_q, content=cont))
                # link the question with form
                db_session.query(FormsQuestions).filter(form_id=form_id).filter(question_id=question_id) \
                    .update({FormsQuestions.question_id: id_q}, synchronize_session=False)
            elif tipo_domanda == "multiple_choice":
                # add the new question
                db_session.add(Questions(text=text_question))
                db_session.commit()
                id_q = (db_session.query(Questions.id).filter(Questions.text == text_question).first())[0]
                db_session.add(MultipleChoiceQuestions(id=id_q))
                db_session.commit()
                db_session.add(TagsQuestions(tag_id=id_t, question_id=id_q))
                # add the possibile answers
                number = req.get("number_answers")

                for i in range(1, int(number) + 1):
                    cont = req.get(str(i))
                    db_session.add(PossibleAnswersM(idPosAnswM=id_q, content=cont))
                # link the question with form
                db_session.query(FormsQuestions).filter(form_id=form_id).filter(question_id=question_id) \
                    .update({FormsQuestions.question_id: id_q}, synchronize_session=False)
            db_session.commit()
        return redirect(url_for('form_management_BP.form_edit', form_id=form_id))

    tags = db_session.query(Tags)
    questions = db_session.query(Questions)
    return render_template("question_add.html", form=form, tags=tags, questions=questions)


# Compiling a specific form
@form_management_BP.route("/<form_id>/viewform", methods=['GET', 'POST'])
@auth_required()
def form_view(form_id):
    form = db_session.query(Forms).filter(Forms.id == form_id).first()
    if request.method == "POST":
        req = request.form
        # check if the user already answered the form
        exist_answers = db_session.query(Answers).filter(Answers.form_id == form_id).filter(
            Answers.user_id == current_user.id).first()
        if exist_answers:
            return render_template("error.html", message="Hai già compilato questo form")
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

    if current_user.id != form.creator_id:
        return render_template("form.html", user=current_user, questions=form.questions, form=form)
    else:
        return render_template("form_edit.html", user=current_user, questions=form.questions, form=form)


# Visualize the answers of a specific form
@form_management_BP.route("/<form_id>/answers")
@auth_required()
def form_answers(form_id):
    answers = db_session.query(Answers).filter(Answers.form_id == form_id)
    total_answers = db_session.query(Answers.user_id).filter(Answers.form_id == form_id).group_by(
        Answers.user_id).count()
    form = db_session.query(Forms).filter(Forms.id == form_id).first()
    return render_template("form_answers.html", user=current_user, answers=answers, form=form,
                           total_answers=total_answers)
