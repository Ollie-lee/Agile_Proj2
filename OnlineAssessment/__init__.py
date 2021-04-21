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
from OnlineAssessment.error_pages.handlers import error_pages
from OnlineAssessment.core.views import core
from OnlineAssessment.users.views import users
from OnlineAssessment.questions.views import questions
from OnlineAssessment.tests.views import tests

# Register blueprint
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
app.register_blueprint(questions)
app.register_blueprint(tests)

# with app.app_context():
#     if db.engine.url.drivername == 'sqlite':
#         Migrate.init_app(app, db, render_as_batch=True)
#     else:
#         Migrate.init_app(app, db)


def checkAnswer(answers, question):
    flag = False
    if len(answers) > 0:
        for answer in answers:
            if answer.question_id == question.id:
                flag = True
    print(flag)
    return flag


app.jinja_env.globals.update(checkAnswer=checkAnswer)
