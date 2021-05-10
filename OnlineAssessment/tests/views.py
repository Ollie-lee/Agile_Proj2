from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from OnlineAssessment import db
from OnlineAssessment.models import Test, Question, Answer
from sqlalchemy.sql.expression import func, select
from OnlineAssessment.tests.forms import AnswerForm, TestForm

tests = Blueprint('tests', __name__)

@tests.route('/assessment')
@login_required
def assessment():
    return render_template('assessment.html')

@tests.route('/create-test')
@login_required
def create_test():
    questions = Question.query.all()[:5]
    test = Test(user_id=current_user.id, questions=questions)
    db.session.add(test)
    db.session.commit()
    flash("Test Created")
    question_num=1
    return redirect(url_for('tests.test', test_id=test.id, question_num=question_num ))

@tests.route('/test/<int:test_id>/<int:question_num>', methods=['GET', 'POST'])
@login_required
def test(test_id, question_num):
    test = Test.query.get_or_404(test_id)
    questions = test.questions
    answers = Answer.query.filter_by(test_id=test_id).all()
    form = AnswerForm()
    testForm = TestForm()
    if form.validate_on_submit():
        # get the current question id
        question_id=form.question.data,
        answer = Answer(
            # get the value of the option selected by the user
            content=form.content.data,
            user_id=current_user.id,
            question_id=form.question.data,
            test_id=test_id,
        )
        db.session.add(answer)
        db.session.commit()
        question_num +=1
        if question_num <= len(questions):
            flash("Answer uploaded!")
            return redirect(url_for('tests.test', test_id=test.id, question_num=question_num ))
        else:
            test.finish = True
            db.session.commit()
            flash("Test submitted!")
            return redirect(url_for('tests.test_results', test_id=test_id))
    #if testForm.validate_on_submit():       
    return render_template('test_question.html', test=test, questions=questions, form=form, answers=answers, question_num=question_num)

# This page shows results after a user completes a test
@tests.route('/test_results/<int:test_id>')
@login_required
def test_results(test_id):
    test = Test.query.get_or_404(test_id)
    answers = test.answers
    questions = test.questions
    return render_template('test_results.html', test=test, answers=answers, questions=questions)

# This page shows all tests results of the user
@tests.route('/my_results')
@login_required
def my_results():
    tests = Test.query.filter_by(user_id=current_user.id).all()
    if tests is None:
        tests = []
    return render_template('my_results.html', tests=tests)


'''
@tests.route('/test/<int:test_id>', methods=['GET', 'POST'])
@login_required
def test(test_id):
    test = Test.query.get_or_404(test_id)
    answers = Answer.query.filter_by(test_id=test_id).all()
    form = AnswerForm()
    testForm = TestForm()
    if form.validate_on_submit():
        answer = Answer(
            content=form.content.data,
            user_id=current_user.id,
            question_id=form.question.data,
            test_id=test_id,
        )
        db.session.add(answer)
        db.session.commit()
        flash("Answer uploaded!")
        return redirect('test/{}'.format(test_id))
    if testForm.validate_on_submit():
        test.finish = True
        db.session.commit()
        flash("Test submitted!")
        return redirect(url_for('core.index'))
    return render_template('test.html', test=test, form=form, answers=answers)
'''