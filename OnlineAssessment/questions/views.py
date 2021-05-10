from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from OnlineAssessment import db
from OnlineAssessment.models import Question
from OnlineAssessment.questions.forms import CreateQuestionForm

questions = Blueprint('questions', __name__)


@questions.route('/create-question', methods=['GET', 'POST'])
@login_required
def create_question():
    form = CreateQuestionForm()

    if form.validate_on_submit():

        question = Question(title=form.title.data,
                            content=form.content.data,
                            correct_answer=form.correct_answer.data,)
        db.session.add(question)
        db.session.commit()
        flash("Question Created")
        return redirect(url_for('core.index'))

    return render_template('create_question.html', form=form)


@questions.route('/<int:question_id>')
@login_required
def question(question_id):
    # grab the requested blog post by id number or return 404
    question = Question.query.get_or_404(question_id)
    return render_template('question.html', question=question)

# delete question
@questions.route('/<int:question_id>', methods=['POST'])
@login_required
def delquestion(question_id):
    form = DeleteQuestionForm()
    if form.validate_on_submit():
        question = Question.query.get(question_id)
        db.session.delete(question)
        db.session.commit()
        flash("Question Deleted.")
        return redirect(url_for('questions.create_question'))
    else:
        return redirect(url_for('questions.question'))
