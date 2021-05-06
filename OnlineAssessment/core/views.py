from OnlineAssessment.models import Question, Test, Answer
from flask_login import current_user, login_required
from flask import render_template, request, Blueprint

# using blueprint to help us do routing
core = Blueprint('core', __name__)


@core.route('/')
def index():
    '''
    This is the home page view.
    '''
    page = request.args.get('page', 1, type=int)
    questions = Question.query.paginate(page=page, per_page=5)
    allQuestions = Question.query.all()
    try:
        tests = Test.query.filter_by(user_id=current_user.id).all()
        answers = Answer.query.filter_by(user_id=current_user.id).all()
    except AttributeError:
        tests = []
        answers = []
    return render_template('index.html', questions=questions, tests=tests, answers=answers, allQuestions=allQuestions)


@core.route('/info')
def info():
    '''
    one promoting the theme and purpose to users;
    '''
    return render_template('info.html')

@core.route('/stats')
def stats():
    '''
    This is the stats view.
    '''
    page = request.args.get('page', 1, type=int)
    questions = Question.query.paginate(page=page, per_page=5)
    allQuestions = Question.query.all()
    try:
        tests = Test.query.filter_by(user_id=current_user.id).all()
        answers = Answer.query.filter_by(user_id=current_user.id).all()
    except AttributeError:
        tests = []
        answers = []
    return render_template('stats.html', questions=questions, tests=tests, answers=answers, allQuestions=allQuestions)