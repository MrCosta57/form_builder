from flask import Blueprint, request, redirect, url_for
from flask_security import auth_required

from form_function import *
form_add_BP = Blueprint('form_add_BP', __name__, template_folder='templates/form', url_prefix='/form')


# Permette di creare o importare un form specificando nome e descrizione
@form_add_BP.route("/form_create", methods=['GET', 'POST'])
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
            db_session.add(Forms(name=nome, dataCreation=datetime.now(),
                                 description=descrizione,
                                 creator_id=current_user.id))
        db_session.commit()
        return redirect(url_for('form_view_BP.form'))

    # GET, passati template per anteprima
    forms_template = db_session.query(Forms).filter((Forms.id == 1) | (Forms.id == 2) | (Forms.id == 3) |
                                                    (Forms.id == 4))
    return render_template("form_create.html", user=current_user, forms=forms_template)


# Add a question to a specific form
@form_add_BP.route("/<form_id>/add_question", methods=['GET', 'POST'])
@auth_required()
@creator_or_admin_role_required
def form_add_question(form_id):
    current_form = db_session.query(Forms).filter(Forms.id == form_id).first()
    if not current_form:
        return render_template("error.html", message="This form not exist")

    # if a request of adding a question is send
    if request.method == "POST":
        req = request.form

        message = question_db("add", req, form_id, -1)  # function that add/edit a question in the db

        if message:
            return render_template("error.html", message=message)
        else:
            # goes to /<form_id>/edit
            return redirect(url_for('form_edit_BP.form_edit', form_id=form_id))

    # GET, necessario passare tutti i tags esistenti per caso di import
    tags = db_session.query(Tags)

    # Questions created by the users
    q = db_session.query(Questions).filter(Questions.id == FormsQuestions.question_id). \
        filter(Forms.creator_id == current_user.id).filter(FormsQuestions.form_id == Forms.id)

    # Questions created by admins
    q2 = db_session.query(Questions).filter(Questions.id == FormsQuestions.question_id). \
        filter(Forms.creator_id == Users.id).filter(FormsQuestions.form_id == Forms.id).filter(Roles.name == "Admin"). \
        filter(Roles.id == RolesUsers.role_id).filter(Users.id == RolesUsers.user_id)

    # Base Questions
    q3 = db_session.query(Questions).filter(Questions.id > 0).filter(Questions.id < 28)

    questions = (q.union(q2)).union(q3)

    return render_template("question_add.html", form=current_form, tags=tags, questions=questions, edit=False)