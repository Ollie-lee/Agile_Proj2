from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class AnswerForm(FlaskForm):
    # grab the date automatically from the Model later
    question = IntegerField('Question', validators=[DataRequired()])
    content = StringField(
        'Content', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class TestForm(FlaskForm):
    # grab the date automatically from the Model later
    submit = SubmitField('Submit')
