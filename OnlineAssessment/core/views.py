from OnlineAssessment.models import Question
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
    return render_template('index.html', questions=questions)


@core.route('/info')
def info():
    '''
    one promoting the theme and purpose to users;
    '''
    return render_template('info.html')
