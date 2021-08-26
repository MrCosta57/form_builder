
from flask import request, redirect, url_for, Blueprint
from flask_security import auth_required
from form_function import *

form_edit_BP = Blueprint('form_edit_BP', __name__, template_folder='templates/form', url_prefix='/form')


# Editing a specific form
@form_edit_BP.route("/<form_id>/edit", methods=['GET', 'POST'])
@auth_required()
@creator_or_admin_role_required
def form_edit(form_id):
    current_form = db_session.query(Forms).filter(Forms.id == form_id).first()
    if not current_form:
        return render_template("error.html", message="This form does not exist")

    # This method represents when the user POST a requeste of delete of a specific question
    if request.method == "POST":
        req = request.form

        id_q = req.get("question")  # Hidden form that grants the id of the question

        db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id). \
            filter(FormsQuestions.question_id == id_q).delete()
        db_session.commit()

        # reload the page
        return redirect(url_for('form_edit_BP.form_edit', form_id=form_id))

    # questions + mandatory
    questions = db_session.query(Questions, FormsQuestions).filter(FormsQuestions.form_id == form_id). \
        filter(Questions.id == FormsQuestions.question_id)

    return render_template("form_edit.html", user=current_user, questions=questions, form=current_form)


@form_edit_BP.route("/<form_id>/<question_id>/flag", methods=['POST'])
@auth_required()
@creator_or_admin_role_required
def edit_mand_or_files(form_id, question_id):
    check_parameters = db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id).\
        filter(FormsQuestions.question_id == question_id).first()
    if not check_parameters:
        return render_template("error.html", message="This form or this question does not exist")

    req = request.form
    if 'allows_file_hidden' in req:
        file = False
        if 'checkBox_file' in req:
            file = True

        db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id). \
            filter(FormsQuestions.question_id == question_id).update({"has_file": file})
        db_session.commit()

    if 'mand_hidden' in req:
        mand = False
        if 'checkBox_mandatory' in req:
            mand = True

        db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id). \
            filter(FormsQuestions.question_id == question_id).update({"mandatory": mand})
        db_session.commit()

    return redirect(url_for("form_edit_BP.form_edit", form_id=form_id))


# Editing a specific form info: name and descprition
@form_edit_BP.route("/<form_id>/editMainInfo", methods=['GET', 'POST'])
@auth_required()
@creator_or_admin_role_required
def form_edit_main_info(form_id):
    current_form = db_session.query(Forms).filter(Forms.id == form_id)
    if not current_form:
        return render_template("error.html", message="This form does not exist")

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
        return redirect(url_for('form_edit_BP.form_edit', form_id=form_id))

    return render_template("form_edit_main_info.html", form=current_form.first())


# Route useful for editing a question or the possibile answers of the question
@form_edit_BP.route("/<form_id>/<question_id>", methods=['GET', 'POST'])
@auth_required()
@creator_or_admin_role_required
def form_edit_question(form_id, question_id):
    current_form = db_session.query(Forms).filter(Forms.id == form_id).first()
    current_question = db_session.query(Questions).filter(Questions.id == question_id).first()

    if (not current_form) or (not current_question):
        return render_template("error.html", message="This form or this question does not exist")

    check_parameters = db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id). \
        filter(FormsQuestions.question_id == question_id).first()
    if not check_parameters:
        return render_template("error.html", message="This question is not present in the current form")

    if request.method == "POST":
        req = request.form

        c = req.get("change")  # Check if the user want to change question or possible answers

        # if the user want to change the possible answers
        if c == 'possible_a':
            if current_question.multiple_choice:
                # add the new question
                q = Questions(text=current_question.text)
                db_session.add(q)
                db_session.commit()

                db_session.add(MultipleChoiceQuestions(id=q.id))
                db_session.commit()

                tags = db_session.query(TagsQuestions).filter(TagsQuestions.question_id == question_id).all
                # link the quuestion with the tag
                for t in tags:
                    db_session.add(TagsQuestions(tag_id=t.tag_id, question_id=q.id))

                # add the possibile answers
                number = req.get("number_answers")  # form input text: how many possible answers?

                for i in range(1, int(number) + 1):
                    cont = req.get(str(i))  # form input text: content of possible answers
                    db_session.add(PossibleAnswersM(idPosAnswM=q.id, content=cont))

                # link the question with form
                db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id). \
                    filter(FormsQuestions.question_id == question_id).update({"question_id": q.id})

            elif current_question.single:

                # add the new question
                q = Questions(text=current_question.text)
                db_session.add(q)
                db_session.commit()

                db_session.add(SingleQuestions(id=q.id))
                db_session.commit()

                tags = db_session.query(TagsQuestions).filter(TagsQuestions.question_id == question_id).all()
                # link the quuestion with the tag
                for t in tags:
                    db_session.add(TagsQuestions(tag_id=t.tag_id, question_id=q.id))

                # add the possibile answers
                number = req.get("number_answers")  # form input text: how many possible answers?

                for i in range(1, int(number) + 1):
                    cont = req.get(str(i))  # form input text: content of possible answers
                    db_session.add(PossibleAnswersS(idPosAnswS=q.id, content=cont))

                # link the question with form
                db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id). \
                    filter(FormsQuestions.question_id == question_id).update({"question_id": q.id})

            db_session.commit()

        # if the user want to change the question we use the function question_db
        else:

            message = question_db("edit", req, form_id, question_id)

            if message:
                return render_template("error.html", message=message)

        # goes to /<form_id>/edit
        return redirect(url_for('form_edit_BP.form_edit', form_id=form_id))

    # We need all the tags and the questions if we want to manage the possibility of import a question
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

    # We pass the number of possible answers that the current question has
    number = 0

    if current_question.single:
        number = db_session.query(PossibleAnswersS).filter(PossibleAnswersS.idPosAnswS == question_id).count()
    elif current_question.multiple_choice:
        number = db_session.query(PossibleAnswersM).filter(PossibleAnswersM.idPosAnswM == question_id).count()

    return render_template("question_add.html", form=current_form, tags=tags, questions=questions, q=current_question,
                           edit=True, number=number)



