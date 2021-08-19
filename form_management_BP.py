from functools import wraps

from flask import render_template, request, redirect, url_for, Blueprint, Response, flash, make_response
from flask_security import current_user, auth_required
from sqlalchemy import and_
from werkzeug.utils import secure_filename

from form_function import *

form_management_BP = Blueprint('form_management_BP', __name__, template_folder='templates/form', url_prefix='/form')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def creator_and_admin_role_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        form_id = kwargs.get('form_id')
        admin_role = db_session.query(Roles).filter(Roles.name == "Admin").first()
        creator = db_session.query(Forms).filter(and_(Forms.creator_id == current_user.id, Forms.id == form_id)).first()
        if not creator or admin_role not in current_user.roles:
            return render_template("error.html", message="You do not have permission to view that page")

        return f(*args, **kwargs)

    return decorated_function


# Endpoint for the list of forms of the current user.
# From here you can: edit the form; copy the link of the form; create a new form; delete a Form
#                    check all the anserw of the form
@form_management_BP.route("/", methods=['GET', 'POST'])
@auth_required()
def form():
    # richiesta in post di eliminare il form, viene passato id attraverso hidden form
    if request.method == 'POST':
        req = request.form
        f_id = req.get("form")

        delete_form(f_id)
        return redirect(url_for('form_management_BP.form'))

    # GET sull'endpoint
    forms_list = db_session.query(Forms).filter(Forms.creator_id == current_user.id)
    return render_template("forms_list.html", user=current_user, forms=forms_list)


# Permette di creare o importare un form specificando nome e descrizione
@form_management_BP.route("/form_create", methods=['GET', 'POST'])
@auth_required()
def form_create():
    if request.method == "POST":
        req = request.form

        imp = req.get("import")  # Per controllare se si vuole importare o no template

        nome = req.get("name")  # nome del form

        # Controlliamo che l'utente non abbia un form con lo stesso nome
        exist_form = db_session.query(Forms).filter(Forms.name == nome).filter(
            Forms.creator_id == current_user.id).first()
        if exist_form:
            return render_template("error.html", message="You have already created a form with this name")

        descrizione = req.get("description")  # descrizione del form

        # caso import template
        if imp == "si":
            template = req.get("template")  # scelta del template da parte dell'utente

            if template == "party":
                template_party(current_user.id, nome, descrizione)
            if template == "events":
                template_events(current_user.id, nome, descrizione)
            if template == "info":
                template_contacts(current_user.id, nome, descrizione)
            if template == "meeting":
                template_meets(current_user.id, nome, descrizione)

        # Creazione di un nuovo form
        else:
            db_session.add(Forms(name=nome, dataCreation=date.today(),
                                 description=descrizione,
                                 creator_id=current_user.id))
        db_session.commit()
        return redirect(url_for('form_management_BP.form'))

    # GET, passati template per anteprima
    forms_template = db_session.query(Forms).filter((Forms.id == 1) | (Forms.id == 2) | (Forms.id == 3) |
                                                    (Forms.id == 4))
    return render_template("form_create.html", user=current_user, forms=forms_template)


# Add a question to a specific form
@form_management_BP.route("/<form_id>/add_question", methods=['GET', 'POST'])
@auth_required()
@creator_and_admin_role_required
def form_add_question(form_id):
    current_form = db_session.query(Forms).filter(Forms.id == form_id).first()

    # if a request of adding a question is send
    if request.method == "POST":
        req = request.form

        message = question_db("add", req, form_id, -1)  # function that add/edit a question in the db

        if message:
            return render_template("error.html", message=message)
        else:
            # goes to /<form_id>/edit
            return redirect(url_for('form_management_BP.form_edit', form_id=form_id))

    # GET, necessario passare tutti i tags e question esistenti per caso di import
    tags = db_session.query(Tags)
    questions = db_session.query(Questions)
    return render_template("question_add.html", form=current_form, tags=tags, questions=questions, edit=False)


# Editing a specific form
@form_management_BP.route("/<form_id>/edit", methods=['GET', 'POST'])
@auth_required()
@creator_and_admin_role_required
def form_edit(form_id):
    current_form = db_session.query(Forms).filter(Forms.id == form_id).first()

    # This method represents when the user POST a requeste of delete of a specific question
    if request.method == "POST":
        req = request.form

        id_q = req.get("question")  # Hidden form that grants the id of the question

        db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id). \
            filter(FormsQuestions.question_id == id_q).delete()
        db_session.commit()

        # reload the page
        return redirect(url_for('form_management_BP.form_edit', form_id=form_id))

    questions = db_session.query(Questions, FormsQuestions).filter(FormsQuestions.form_id == form_id).filter(Questions.id == FormsQuestions.question_id)
    return render_template("form_edit.html", user=current_user, questions=questions, form=current_form)


# @form_management_BP.route("/<form_id>/<question_id>/flag", methods=['POST'])
# @auth_required()
# def edit_mand_or_files:
#    if 'checkBox_file' in request.form:
#        if request.form.get('checkBox_file'):
#        # TODO deve comportarsi come una add question in teoria
#    else if 'checkBox_mand' in request.form:
#
#    return redirect(url_for("form_management_BP.form_edit"))

# Editing a specific form info: name and descprition
@form_management_BP.route("/<form_id>/editMainInfo", methods=['GET', 'POST'])
@auth_required()
@creator_and_admin_role_required
def form_edit_main_info(form_id):
    current_form = db_session.query(Forms).filter(Forms.id == form_id)

    # Request of editing name and description
    if request.method == 'POST':
        req = request.form

        # Controlliamo che l'utente non abbia un form con lo stesso nome
        exist_form = db_session.query(Forms).filter(Forms.name == req.get("name")).filter(
            Forms.creator_id == current_user.id).filter(Forms.id != form_id).first()
        if exist_form:
            return render_template("error.html", message="You have already created a form with this name")

        current_form.update({"name": req.get("name"), "description": req.get("description")})
        db_session.commit()

        # goes to /<form_id>/edit
        return redirect(url_for('form_management_BP.form_edit', form_id=form_id))

    return render_template("form_edit_main_info.html", form=current_form.first())


# Route useful for editing a question or the possibile answers of the question
@form_management_BP.route("/<form_id>/<question_id>", methods=['GET', 'POST'])
@auth_required()
@creator_and_admin_role_required
def form_edit_question(form_id, question_id):
    current_form = db_session.query(Forms).filter(Forms.id == form_id).first()
    current_question = db_session.query(Questions).filter(Questions.id == question_id).first()

    if request.method == "POST":
        req = request.form

        c = req.get("change")  # Check if the user want to change question or possible answers

        # if the user want to change the possible answers
        if c == 'possible_a':
            if current_question.multiple_choice:
                # cancelliamo i vecchi dati
                db_session.query(PossibleAnswersM).filter(PossibleAnswersM.idPosAnswM == question_id).delete()
                db_session.commit()

                # Inseriamo i nuovi
                number = req.get("number_answers")

                for i in range(1, int(number) + 1):
                    cont = req.get(str(i))
                    db_session.add(PossibleAnswersM(idPosAnswM=question_id, content=cont))
            elif current_question.single:
                # cancelliamo i vecchi dati
                db_session.query(PossibleAnswersS).filter(PossibleAnswersS.idPosAnswS == question_id).delete()
                db_session.commit()

                # Inseriamo i nuovi
                number = req.get("number_answers")

                for i in range(1, int(number) + 1):
                    cont = req.get(str(i))
                    db_session.add(PossibleAnswersS(idPosAnswS=question_id, content=cont))

            db_session.commit()

        # if the user want to change the question we use the function question_db
        else:

            message = question_db("edit", req, form_id, question_id)

            if message:
                return render_template("error.html", message=message)

        # goes to /<form_id>/edit
        return redirect(url_for('form_management_BP.form_edit', form_id=form_id))

    # We need all the tags and the questions if we want to manage the possibility of import a question
    tags = db_session.query(Tags)
    questions = db_session.query(Questions)

    # We pass the number of possible answers that the current question has
    number = 0

    if current_question.single:
        number = db_session.query(PossibleAnswersS).filter(PossibleAnswersS.idPosAnswS == question_id).count()
    elif current_question.multiple_choice:
        number = db_session.query(PossibleAnswersM).filter(PossibleAnswersM.idPosAnswM == question_id).count()

    return render_template("question_add.html", form=current_form, tags=tags, questions=questions, q=current_question,
                           edit=True, number=number)


# Compiling a specific form
@form_management_BP.route("/<form_id>/viewform", methods=['GET', 'POST'])
@auth_required()
def form_view(form_id):
    current_form = db_session.query(Forms).filter(Forms.id == form_id).first()

    # check if the user already answered the form
    exist_answers = db_session.query(Answers).filter(Answers.form_id == form_id).filter(
        Answers.user_id == current_user.id).first()
    if exist_answers:
        return render_template("error.html", message="You have already filled out this form")

    if request.method == "POST":
        # Check if the uploaded files have the requirements before store them and store questions
        open_question_file_check = db_session.query(OpenQuestions.id).join(FormsQuestions,
                                                                           OpenQuestions.id == FormsQuestions.question_id) \
            .filter(FormsQuestions.form_id == form_id).filter(OpenQuestions.has_file).all()
        for tmp_id in open_question_file_check:
            file = request.files['file_' + str(tmp_id[0])]
            if file:
                filename = secure_filename(file.filename)
                if file.filename == '':
                    flash('No selected file in some questions', 'file_error')
                    return redirect(request.url)
                mimetype = file.mimetype
                if not filename or not mimetype:
                    flash('Bad uploads!', 'file_error')
                    return redirect(request.url)
                if not allowed_file(file.filename):
                    flash('Some file are not allowed', 'file_error')
                    return redirect(request.url)

        # If a user answers the form we save the POST info
        req = request.form
        # Get for every answered question
        for q in current_form.questions:
            if not q.multiple_choice:
                text = [req.get(str(q.id))]
            else:
                text = req.getlist(str(q.id))  # if is a multiple choice question we get multiple answers

            # We add the object: answers
            ans = Answers(form_id=form_id, question_id=q.id, user_id=current_user.id)
            db_session.add(ans)
            db_session.commit()

            # Check if the question is open question and if it allows file adding
            for tmp in q.open:
                if tmp.has_file:
                    # File memorization (the name and the extension was checked before)
                    file = request.files['file_' + str(tmp.id)]
                    if file:
                        filename = secure_filename(file.filename)
                        mimetype = file.mimetype
                        virtual_file = Files(data=file.read(), name=filename, mimetype=mimetype, answer_id=ans.id)
                        db_session.add(virtual_file)
                        db_session.commit()

            # we add all the answers (if the users leave a blank multiple choice/single answer we don't memorize
            # anything)
            for t in text:
                if t:
                    db_session.add(SeqAnswers(id=ans.id, content=t))
                elif ans.question.open:
                    db_session.add(SeqAnswers(id=ans.id, content='blank'))

            db_session.commit()

        return redirect(url_for('home'))

    # The creator of a form can only edit the form
    questions = db_session.query(Questions, FormsQuestions).filter(FormsQuestions.form_id == form_id).filter(Questions.id == FormsQuestions.question_id)
    if current_user.id != current_form.creator_id:
        return render_template("form_view.html", user=current_user, questions=questions, form=current_form)
    else:
        return render_template("form_edit.html", user=current_user, questions=questions, form=current_form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Visualize the answers of a specific form
@form_management_BP.route("/<form_id>/answers")
@auth_required()
@creator_and_admin_role_required
def form_answers(form_id):
    # List of all the answers of this for
    answers = db_session.query(Answers, Files).join(Files, Answers.id == Files.answer_id, isouter=True).filter(
        Answers.form_id == form_id)
    total_answers = db_session.query(Answers.user_id).filter(Answers.form_id == form_id).group_by(
        Answers.user_id).count()

    current_form = db_session.query(Forms).filter(Forms.id == form_id).first()

    return render_template("form_answers.html", user=current_user, answers=answers, form=current_form,
                           total_answers=total_answers)


@form_management_BP.route("/<form_id>/answers/<answer_id>/<user_id>")
@auth_required()
@creator_and_admin_role_required
def view_files(form_id, answer_id, user_id):
    file = db_session.query(Files).filter(Answers.user_id == user_id).filter(Files.answer_id == answer_id).first()
    response = make_response(file.data)
    response.headers['Content-Type'] = file.mimetype
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % file.name
    return response


@form_management_BP.route("/<form_id>/download_csv")
@auth_required()
@creator_and_admin_role_required
def download_csv_answers(form_id):
    answers_all = db_session.query(Users.username, Questions.text, SeqAnswers.content).filter(
        Answers.form_id == form_id).filter(
        Answers.id == SeqAnswers.id).filter(Users.id == Answers.user_id).filter(Questions.id == Answers.question_id)
    csv = ''
    for a in answers_all:
        csv = csv + a.username + ',' + a.text + ',' + a.content + '\n'

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=answers.csv"})
