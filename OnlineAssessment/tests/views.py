from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from OnlineAssessment import db
from OnlineAssessment.models import Test, Question, Answer
from sqlalchemy.sql.expression import func, select
from OnlineAssessment.tests.forms import AnswerForm

tests = Blueprint('tests', __name__)


@tests.route('/create-test')
@login_required
def create_test():
    questions = Question.query.all()[:5]
    # print(questions)
    # print(current_user)
    test = Test(user_id=current_user.id, questions=questions)
    # print(test)
    db.session.add(test)
    db.session.commit()
    flash("Test Created")
    return redirect(url_for('core.index'))


@tests.route('/test/<int:test_id>', methods=['GET', 'POST'])
@login_required
def test(test_id):
    test = Test.query.get_or_404(test_id)
    answers = Answer.query.filter_by(test_id=test_id).all()
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(
            content=form.content.data,
            user_id=current_user.id,
            question_id=form.question.data,
            test_id=test_id,
        )
        db.session.add(answer)
        db.session.commit()
        flash("Question Created")
        return redirect('test/{}'.format(test_id))
    return render_template('test.html', test=test, form=form, answers=answers)
