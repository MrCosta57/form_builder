from database import db_session
from models import *
from datetime import date


# function that add or edit a question in the db (with tags and possible answers)
def question_db(type, req, form_id, question_id):
    # Question already exists
    if req.get("choose") == "si":
        id_q = req.get("question_choose")
        if type == 'add':
            db_session.add(FormsQuestions(form_id=form_id, question_id=id_q))
        elif type == 'edit':
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
            if type == 'add':
                db_session.add(FormsQuestions(form_id=form_id, question_id=id_q))
            elif type == 'edit':
                db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id).filter(FormsQuestions.question_id == question_id) \
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
            if type == 'add':
                db_session.add(FormsQuestions(form_id=form_id, question_id=id_q))
            elif type == 'edit':
                db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id).filter(FormsQuestions.question_id == question_id) \
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
            if type == 'add':
                db_session.add(FormsQuestions(form_id=form_id, question_id=id_q))
            elif type == 'edit':
                db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id).filter(FormsQuestions.question_id == question_id) \
                    .update({FormsQuestions.question_id: id_q}, synchronize_session=False)
        db_session.commit()


# TEMPLATE FUNCTION
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