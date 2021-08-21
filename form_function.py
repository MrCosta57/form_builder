from jinja2 import Template

from database import db_session
from models import *
from datetime import date


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
                        Questions(text="Parteciperai all'evento?"),
                        Questions(text="Inserisci un breve commento"),
                        Questions(text="Valuta questo sondaggio"),
                        Questions(text="Come hai conosciuto questo evento?"),
                        Questions(text="Hai intolleranze alimentari, se si quali?"),
                        Questions(text="Che corsi hai seguito? "),
                        Questions(text="che materie studi?"),
                        Questions(text="Fai la raccolta differenziata?"),
                        Questions(text="Quali stati hai visitato?"),
                        Questions(text="Possiedi animali?"),
                        Questions(text="Animale preferito"),
                        Questions(text="Carica il tuo CV")])
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
                        OpenQuestions(id=27, has_file=True),

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
                        TagsQuestions(tag_id=6, question_id=26),
                        TagsQuestions(tag_id=5, question_id=27)])
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


# function that add or edit a question in the db (with tags and possible answers)
def question_db(type, req, form_id, question_id):
    # mandatory
    mand = req.get("mandatory")
    if mand == "on":
        mand = True
    else:
        mand = False

    # Question already exists
    if req.get("choose") == "si":
        id_q = req.get("question_choose")  # Menu a tendina con lista domande

        # add or edit
        if type == 'add':
            db_session.add(FormsQuestions(form_id=form_id, question_id=id_q, mandatory=mand))
        elif type == 'edit':
            db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id).filter(
                FormsQuestions.question_id == question_id) \
                .update({FormsQuestions.question_id: id_q, FormsQuestions.mandatory: mand}, synchronize_session=False)
        db_session.commit()

    # new Question
    else:
        tag = req.get("tag_choose")  # Menu tendina: scelta tag

        # create new Tag
        if tag == "nuovo":
            new_tag = req.get("tag_aggiunto")  # form input text tag
            # add the tag to the database
            if db_session.query(Tags).filter(Tags.argument == new_tag).first():
                return "THIS TAG ALREADY EXISTS"
            db_session.add(Tags(argument=new_tag))
            db_session.commit()
            tag = new_tag

        tipo_domanda = req.get("tipo_domanda")   # Menu tendina: open, single, multiple_choice
        text_question = req.get("text_question")  # form input text, domanda

        id_t = (db_session.query(Tags.id).filter(Tags.argument == tag).first())[0]  # Trova id del tag selezionato

        # Type of the question
        if tipo_domanda == "open":

            # Add the question
            q = Questions(text=text_question)
            db_session.add(q)
            db_session.commit()

            has_file = False
            if req.get('file_choose') == 'si':
                has_file = True
            db_session.add(OpenQuestions(id=q.id, has_file=has_file))
            db_session.commit()

            # link the question with tag
            db_session.add(TagsQuestions(tag_id=id_t, question_id=q.id))

            # link the question with the form
            if type == 'add':
                db_session.add(FormsQuestions(form_id=form_id, question_id=q.id, mandatory=mand))
            elif type == 'edit':
                db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id).filter(
                    FormsQuestions.question_id == question_id) \
                    .update({FormsQuestions.question_id: q.id, FormsQuestions.mandatory: mand}, synchronize_session=False)

        elif tipo_domanda == "single":

            # add the new question
            q = Questions(text=text_question)
            db_session.add(q)
            db_session.commit()
            db_session.add(SingleQuestions(idS=q.id))
            db_session.commit()

            # link the quuestion with the tag
            db_session.add(TagsQuestions(tag_id=id_t, question_id=q.id))

            # add the possibile answers
            number = req.get("number_answers")  # form input text: how many possible answers?

            for i in range(1, int(number) + 1):
                cont = req.get(str(i))  # form input text: content of possible answers
                db_session.add(PossibleAnswersS(idPosAnswS=q.id, content=cont))

            # link the question with form
            if type == 'add':
                db_session.add(FormsQuestions(form_id=form_id, question_id=q.id, mandatory=mand))
            elif type == 'edit':
                db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id).filter(
                    FormsQuestions.question_id == question_id) \
                    .update({FormsQuestions.question_id: q.id, FormsQuestions.mandatory: mand}, synchronize_session=False)

        elif tipo_domanda == "multiple_choice":
            # add the new question
            q = Questions(text=text_question)
            db_session.add(q)
            db_session.commit()
            db_session.add(MultipleChoiceQuestions(id=q.id))
            db_session.commit()

            # link the quuestion with the tag
            db_session.add(TagsQuestions(tag_id=id_t, question_id=q.id))

            # add the possibile answers
            number = req.get("number_answers")  # form input text: how many possible answers?

            for i in range(1, int(number) + 1):
                cont = req.get(str(i))  # form input text: content of possible answers
                db_session.add(PossibleAnswersM(idPosAnswM=q.id, content=cont))

            # link the question with form
            if type == 'add':
                db_session.add(FormsQuestions(form_id=form_id, question_id=q.id, mandatory=mand))
            elif type == 'edit':
                db_session.query(FormsQuestions).filter(FormsQuestions.form_id == form_id).filter(
                    FormsQuestions.question_id == question_id) \
                    .update({FormsQuestions.question_id: q.id, FormsQuestions.mandatory: mand}, synchronize_session=False)

        db_session.commit()


def delete_form(f_id):
    # elimino link tra domande e form
    db_session.query(FormsQuestions).filter(FormsQuestions.form_id == f_id).delete()
    db_session.commit()

    # elimino tutte le risposte del form
    answers = db_session.query(Answers).filter(Answers.form_id == f_id)
    for a in answers:
        db_session.query(SeqAnswers).filter(SeqAnswers.id == a.id).delete()
    answers.delete()

    # infine elimino il form
    db_session.query(Forms).filter(Forms.id == f_id).delete()
    db_session.commit()


# TEMPLATE FUNCTION
def template_party(id_user, name, description):
    f = Forms(name=name, dataCreation=date.today(),
              description=description,
              creator_id=id_user)
    db_session.add(f)
    db_session.commit()

    db_session.add_all([FormsQuestions(form_id=f.id, question_id=1),
                        FormsQuestions(form_id=f.id, question_id=2),
                        FormsQuestions(form_id=f.id, question_id=11),
                        FormsQuestions(form_id=f.id, question_id=15),
                        FormsQuestions(form_id=f.id, question_id=13),
                        FormsQuestions(form_id=f.id, question_id=16)])
    db_session.commit()


def template_meets(id_user, name, description):
    f = Forms(name=name, dataCreation=date.today(),
              description=description,
              creator_id=id_user)
    db_session.add(f)
    db_session.commit()

    db_session.add_all([FormsQuestions(form_id=f.id, question_id=1),
                        FormsQuestions(form_id=f.id, question_id=2),
                        FormsQuestions(form_id=f.id, question_id=4),
                        FormsQuestions(form_id=f.id, question_id=7),
                        FormsQuestions(form_id=f.id, question_id=8),
                        FormsQuestions(form_id=f.id, question_id=13),
                        FormsQuestions(form_id=f.id, question_id=20, mandatory=True),
                        FormsQuestions(form_id=f.id, question_id=27)])
    db_session.commit()


def template_events(id_user, name, description):
    f = Forms(name=name, dataCreation=date.today(),
              description=description,
              creator_id=id_user)
    db_session.add(f)
    db_session.commit()

    db_session.add_all([FormsQuestions(form_id=f.id, question_id=1),
                        FormsQuestions(form_id=f.id, question_id=2),
                        FormsQuestions(form_id=f.id, question_id=3),
                        FormsQuestions(form_id=f.id, question_id=5),
                        FormsQuestions(form_id=f.id, question_id=16),
                        FormsQuestions(form_id=f.id, question_id=20)])
    db_session.commit()


def template_contacts(id_user, name, description):
    f = Forms(name=name, dataCreation=date.today(),
              description=description,
              creator_id=id_user)
    db_session.add(f)
    db_session.commit()

    db_session.add_all([FormsQuestions(form_id=f.id, question_id=1),
                        FormsQuestions(form_id=f.id, question_id=2),
                        FormsQuestions(form_id=f.id, question_id=5),
                        FormsQuestions(form_id=f.id, question_id=6),
                        FormsQuestions(form_id=f.id, question_id=7),
                        FormsQuestions(form_id=f.id, question_id=8),
                        FormsQuestions(form_id=f.id, question_id=9),
                        FormsQuestions(form_id=f.id, question_id=10)])
    db_session.commit()
