from flask import render_template,request,Blueprint
from puppycompanyblog.models import BlogPost

core = Blueprint('core', __name__)
