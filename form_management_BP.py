from datetime import date
from flask import render_template, request, redirect, url_for, Blueprint
from flask_security import current_user, auth_required
from database import db_session
from models import *
from form_function import *

form_management_BP = Blueprint('form_management_BP', __name__, template_folder='templates/form', url_prefix='/form')


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

    forms_template = db_session.query(Forms)
    return render_template("form_create.html", user=current_user, forms=forms_template)


# Add a question to a specific form
@form_management_BP.route("/<form_id>/add_question", methods=['GET', 'POST'])
def form_add_question(form_id):
    form = db_session.query(Forms).filter(Forms.id == form_id).first()
    if request.method == "POST":
        req = request.form
        question_db("add", req, form_id, -1)
        return redirect(url_for('form_management_BP.form_edit', form_id=form_id))

    tags = db_session.query(Tags)
    questions = db_session.query(Questions)
    return render_template("question_add.html", form=form, tags=tags, questions=questions, edit=False)


# Editing a specific form
@form_management_BP.route("/<form_id>/edit")
@auth_required()
def form_edit(form_id):
    form = db_session.query(Forms).filter(Forms.id == form_id).first()
    return render_template("form_edit.html", user=current_user, questions=form.questions, form=form)


@form_management_BP.route("/<form_id>/<question_id>", methods=['GET', 'POST'])
def form_edit_question(form_id, question_id):
    form = db_session.query(Forms).filter(Forms.id == form_id).first()
    q = db_session.query(Questions).filter(Questions.id == question_id).first()
    if request.method == "POST":
        req = request.form
        c = req.get("change")
        if c == 'possible_a':
            if q.multiple_choice:
                db_session.query(PossibleAnswersM).filter(PossibleAnswersM.idPosAnswM == question_id).delete()
                db_session.commit()
                number = req.get("number_answers")

                for i in range(1, int(number) + 1):
                    cont = req.get(str(i))
                    db_session.add(PossibleAnswersM(idPosAnswM=question_id, content=cont))
            elif q.single:
                db_session.query(PossibleAnswersS).filter(PossibleAnswersS.idPosAnswS == question_id).delete()
                db_session.commit()
                number = req.get("number_answers")

                for i in range(1, int(number) + 1):
                    cont = req.get(str(i))
                    db_session.add(PossibleAnswersS(idPosAnswS=question_id, content=cont))
            db_session.commit()
        else:
            question_db("edit", req, form_id, question_id)
        return redirect(url_for('form_management_BP.form_edit', form_id=form_id))

    tags = db_session.query(Tags)
    questions = db_session.query(Questions)
    q = db_session.query(Questions).filter(Questions.id == question_id).first()
    number = 0
    if q.single:
        number = db_session.query(PossibleAnswersS).filter(PossibleAnswersS.idPosAnswS == question_id).count()
    elif q.multiple_choice:
        number = db_session.query(PossibleAnswersM).filter(PossibleAnswersM.idPosAnswM == question_id).count()
    return render_template("question_add.html", form=form, tags=tags, questions=questions, q=q, edit=True, number=number)


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
