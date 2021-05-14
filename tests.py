import unittest
from OnlineAssessment import db, app
from OnlineAssessment.models import User, Question, Answer, Test


class TestCase(unittest.TestCase):
    ####################### set up test ###############################
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ####################### User Model Unit Test ###############################
    def test_password_hashing(self):
        u = User(username='test', email='test@gmail.com', password='password', role='ADMIN')	
        self.assertFalse(u.check_password('wrongPassword'))
        self.assertTrue(u.check_password('password'))
        
    def test_initial_answers(self):
        u = User(username='test', email='test@gmail.com', password='password', role='ADMIN')	
        self.assertEqual(u.answers, [])
        
    def test_user_creating(self):
        u = User(username='test', email='test@gmail.com', password='password', role='ADMIN')	
        db.session.add(u)
        db.session.commit()
        user = User.query.filter_by(username='test')
        self.assertEqual(user.count(), 1)
        self.assertEqual(user.first().username, 'test')
        self.assertEqual(user.first().email, 'test@gmail.com')
        self.assertEqual(user.first().role, 'ADMIN')    
        

    ####################### Question Model Unit Test ###############################
    def test_question_creating(self):
        q = Question(title='title', content='content', correct_answer='correct_answer')	
        db.session.add(q)
        db.session.commit()
        question = Question.query.filter_by(title='title')
        self.assertEqual(question.count(), 1)
        self.assertEqual(question.first().title, 'title')
        self.assertEqual(question.first().content, 'content')
        self.assertEqual(question.first().correct_answer, 'correct_answer')

    def test_question_deleting(self):
        q = Question(title='title', content='content', correct_answer='correct_answer')	
        db.session.add(q)
        db.session.commit()
        db.session.delete(q)
        db.session.commit()
        newQuestion = Question.query.filter_by(title='title')
        self.assertEqual(newQuestion.count(), 0)
        
    ####################### Test Model Unit Test ###############################
    def test_test_creating(self):
        u = User(username='test', email='test@gmail.com', password='password', role='ADMIN')	
        db.session.add(u)
        db.session.commit()
        q = Question(title='title', content='content', correct_answer='correct_answer')	
        db.session.add(q)
        db.session.commit()        
        t = Test(user_id=u.id, questions=[q])
        db.session.add(t)
        db.session.commit() 
        test = Test.query.filter_by(user_id=u.id)
        self.assertEqual(test.count(), 1)

    ####################### Answer Model Unit Test ###############################
    def test_answer_creating(self):
        u = User(username='test', email='test@gmail.com', password='password', role='ADMIN')	
        db.session.add(u)
        db.session.commit()
        q = Question(title='title', content='content', correct_answer='correct_answer')	
        db.session.add(q)
        db.session.commit()        
        t = Test(user_id=u.id, questions=[q])
        db.session.add(t)
        db.session.commit() 
        a = Answer(content='content', user_id=u.id, question_id=q.id, test_id=t.id)	
        
        db.session.add(a)
        db.session.commit()
        answer = Answer.query.filter_by(content='content')
        self.assertEqual(answer.count(), 1)
        self.assertEqual(answer.first().content, 'content')

if __name__ == '__main__':
    unittest.main(verbosity=2)
