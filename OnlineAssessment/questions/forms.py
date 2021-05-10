from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreateQuestionForm(FlaskForm):
    # grab the date automatically from the Model later
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    correct_answer = TextAreaField('Correct Answer', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteQuestionForm(FlaskForm):
    submit = SubmitField('Delete')
