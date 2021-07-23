from database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
    String, ForeignKey


class Roles(Base, RoleMixin):
    __tablename__ = 'roles'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class Users(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    date = Column(DateTime(), nullable=False)

    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())

    roles = relationship('Roles', secondary='roles_users', backref=backref('users', lazy='dynamic'))
    forms_created = relationship('Forms', back_populates='creator')
    answered_forms = relationship('Forms', secondary='filled_by', back_populates='user_answer')


class Forms(Base):
    __tablename__ = 'forms'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    dataCreation = Column(DateTime())
    description = Column(String(255))
    creator_id = Column(Integer, ForeignKey(Users.id), nullable=False)

    creator = relationship('Users', back_populates="forms_created")
    user_answer = relationship('Users', secondary='filled_by', back_populates='answered_forms')
    questions = relationship('Questions', secondary='forms_questions')
    answers = relationship('Answers', back_populates='form')


# Tables for n to n relationship
class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('users.id'))
    role_id = Column('role_id', Integer(), ForeignKey('roles.id'))


class FilledBy(Base):
    __tablename__ = 'filled_by'
    user_id = Column('user_id', Integer(), ForeignKey('users.id'), primary_key=True)
    form_id = Column('form_id', Integer(), ForeignKey('forms.id'), primary_key=True)


class TagsQuestions(Base):
    __tablename__ = 'tags_questions'
    tag_id = Column('tag_id', Integer(), ForeignKey('tags.id'), primary_key=True)
    question_id = Column('question_id', Integer(), ForeignKey('questions.id'), primary_key=True)


class FormsQuestions(Base):
    __tablename__ = 'forms_questions'
    form_id = Column('form_id', Integer(), ForeignKey('forms.id'), primary_key=True)
    question_id = Column('question_id', Integer(), ForeignKey('questions.id'), primary_key=True)


class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    argument = Column(String(255))

    questions = relationship('Questions', secondary='tags_questions', back_populates='tags')


class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    file = Column(String(255))
    text = Column(String(255))

    tags = relationship('Tags', secondary='tags_questions', back_populates='questions')
    answers = relationship('Answers', back_populates='question')
    multiple_choice = relationship('MultipleChoiceQuestions')
    single = relationship('SingleQuestions')
    open = relationship('OpenQuestions')


class SingleQuestions(Base):
    __tablename__ = 'single_question'
    idS = Column(Integer, ForeignKey(Questions.id), primary_key=True)


class PossibleAnswersS(Base):
    __tablename__ = 'possible_answers_s'
    idPosAnswS = Column(Integer, ForeignKey(SingleQuestions.idS), primary_key=True)
    content = Column(String, primary_key=True)


class OpenQuestions(Base):
    __tablename__ = 'open_questions'
    id = Column(Integer,  ForeignKey(Questions.id), primary_key=True)


class MultipleChoiceQuestions(Base):
    __tablename__ = 'multiple_choice_question'
    id = Column(Integer, ForeignKey(Questions.id), primary_key=True)


class PossibleAnswersM(Base):
    __tablename__ = 'possible_answers_m'
    idPosAnswM = Column(Integer, ForeignKey(MultipleChoiceQuestions.id), primary_key=True)
    content = Column(String, primary_key=True)


class Answers(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    form_id = Column(Integer, ForeignKey(Forms.id), nullable=False)
    question_id = Column(Integer, ForeignKey(Questions.id), nullable=False)

    question = relationship('Questions', back_populates='answers')
    text = relationship('SeqAnswers', back_populates='info')
    form = relationship('Forms', back_populates='answers')


class SeqAnswers(Base):
    __tablename__ = 'seq_answers'
    id = Column(Integer, ForeignKey(Answers.id), primary_key=True)
    content = Column(String, primary_key=True)

    info = relationship('Answers', back_populates='text')
