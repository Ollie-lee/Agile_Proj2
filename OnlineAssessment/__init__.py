
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

# set environment variables at the command line
app.config['SECRET_KEY'] = 'agileWeb'

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# entry point of db
db = SQLAlchemy(app)
Migrate(app, db)


# Login Config
login_manager = LoginManager()

# pass app to the login manager
login_manager.init_app(app)

# what view to go to when login.
login_manager.login_view = "users.login"


# use blueprint to route
from OnlineAssessment.tests.views import tests
from OnlineAssessment.questions.views import questions
from OnlineAssessment.users.views import users
from OnlineAssessment.core.views import core
from OnlineAssessment.error_pages.handlers import error_pages

# Register blueprint
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
app.register_blueprint(questions)
app.register_blueprint(tests)


def checkAnswer(answers, question):
    flag = False
    if len(answers) > 0:
        for answer in answers:
            if answer.question_id == question.id:
                flag = True
    return flag


def mapCorrectAnswer(question):
    return question.correct_answer


def isAnswerCorrect(answer, questions):
    correctAnswers = map(mapCorrectAnswer, questions)
    return (answer.content in correctAnswers)


def calculateScore(answers, test, questions):
    score = 0
    correctAnswers = []
    for answer in answers:
        if isAnswerCorrect(answer, questions):
            correctAnswers.append(answer)
    if len(correctAnswers) > 0:
        for correctAnswer in correctAnswers:
            if correctAnswer.test_id == test.id:
                score += 1
    return score


app.jinja_env.globals.update(checkAnswer=checkAnswer)
