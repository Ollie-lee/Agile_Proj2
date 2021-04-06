from flask import render_template,request,Blueprint

#using blueprint to help us do routing
core = Blueprint('core', __name__)

@core.route('/')
def index():
    '''
    This is the home page view.
    '''
    return render_template('index.html')

@core.route('/info')
def info():
    '''
    one promoting the theme and purpose to users;
    '''
    return render_template('info.html')