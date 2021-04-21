from sqlalchemy.sql.expression import true
from OnlineAssessment import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# load the current user and get their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    # Create a table in the db
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Enum('USER', 'ADMIN'),
                     nullable=False, server_default=("USER"))
    # This connects Answer to a User Author.
    answers = db.relationship('Answer', backref='author_answers', lazy=True)

    def __init__(self, email, username, password, role):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"UserName: {self.username}"


class Question(db.Model):
    # Create a table in the db
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.String(140), nullable=False)
    # This connects Question to a Answer, specified by user
    answers = db.relationship('Answer', backref='question', lazy=True)
    # Specified by admin
    correct_answer = db.Column(db.String(140), nullable=False)

    def __init__(self, title, content, correct_answer):
        self.title = title
        self.content = content
        self.correct_answer = correct_answer

    def __repr__(self):
        return f"Question Id: {self.id} --- Title: {self.title} --- Content: {self.content} --- user_id: {self.correct_answer}"


class Answer(db.Model):
    # Create a table in the db
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    # connect the Answer to a particular author/question
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'questions.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(140), nullable=False)
    finish = db.Column(db.Boolean, default=False, nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)

    def __init__(self, content, user_id, question_id, test_id):
        self.content = content
        self.user_id = user_id
        self.question_id = question_id
        self.test_id = test_id
        self.finish = True

    def __repr__(self):
        return f"Answer Id: {self.id} --- Date: {self.date} --- Content: {self.content} --- Author: {self.user_id} --- Question: {self.question_id}"


test_question_relation = db.Table('test_question_relation',
                                  db.Column('question_id', db.Integer,
                                            db.ForeignKey('questions.id')),
                                  db.Column('test_id', db.Integer,
                                            db.ForeignKey('tests.id')),
                                  )


class Test(db.Model):
    # Create a table in the db
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    # connect the Answer to a particular author/question
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    questions = db.relationship('Question', secondary=test_question_relation, backref=db.backref(
        'questions_tests', lazy='dynamic'))
    answers = db.relationship('Answer', backref='test_answers', lazy=True)
    finish = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, user_id, questions):
        self.user_id = user_id
        self.questions = questions

    def __repr__(self):
        return f"test Id: {self.id} --- questions: {self.questions} --- user: {self.user_id} "
