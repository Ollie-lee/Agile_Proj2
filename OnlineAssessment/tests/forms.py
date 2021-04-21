from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class AnswerForm(FlaskForm):
    # grab the date automatically from the Model later
    user = IntegerField('User', validators=[DataRequired()])
    question = StringField('Question', validators=[DataRequired()])
    content = StringField(
        'Content', validators=[DataRequired()])
    submit = SubmitField('Submit')
