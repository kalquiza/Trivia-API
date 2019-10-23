import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_category = Category(
            type="Test"
        )

        self.new_question = Question(
            question="Why did the chicken cross the road?",
            answer="To get to the other side.",
            difficulty=1,
            category=1
        )

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            # insert a category and corresponding question
            self.db.session.add(self.new_category)
            self.new_question.category=self.db.session.query(Category).one().id
            self.db.session.add(self.new_question)
            self.db.session.commit()

    def tearDown(self):
        """Executed after each test"""
        # clear all table entries
        with self.app.app_context():
            self.db.session.query(Question).delete()
            self.db.session.query(Category).delete()
            self.db.session.commit()


    """ Test endpoint GET /categories"""
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    def test_404_get_categories_no_categories_(self):
        with self.app.app_context():
            self.db.session.query(Category).delete()
            self.db.session.commit()
                    
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')    


    """ Test endpoint GET /questions"""
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_get_questions_invalid_page(self):
        res = self.client().get('questions/?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')    


    """ Test endpoint DELETE /questions"""
    def test_delete_question(self):
        with self.app.app_context():
            question_id = self.db.session.query(Question).one().id

        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)

    def test_422_request_delete_nonexisting_question(self):
        question_id = 0
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')


    """ Test endpoint POST /questions"""
    def test_create_question(self):
        new_question = "Why did I create this question?"
        new_answer = "To test the application for expected behavior."
        new_category = 1
        new_difficulty = 1

        res = self.client().post('/questions', json={"question": new_question, "answer": new_answer, "category": new_category, "difficulty": new_difficulty})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_422_request_create_question_empty_payload(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')


    """ Test endpoint POST /questions/search"""
    def test_search_questions(self):
        res = self.client().post('/questions/search', json={"searchTerm": "?"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_search_questions_empty_payload(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')


    """ Test endpoint POST /questions/<int:category_id>/questions"""
    def test_get_questions_by_category(self):
        with self.app.app_context():
            category_id = int(self.db.session.query(Question).one().category)-1

        res = self.client().get('/categories/{}/questions'.format(category_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['current_category'])

    def test_404_get_questions_by_category_invalid_category_id(self):
        category_id = 0
        res = self.client().get('/categories/{}/questions'.format(category_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')    


    """ Test endpoint POST /quizzes"""
    def test_get_quiz_questions(self):
        with self.app.app_context():
            category_id = int(self.db.session.query(Question).one().category)-1

        res = self.client().post('/quizzes', json={"previous_questions":[],"quiz_category":{"type":"Test","id":category_id}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['previous_questions'])

    def test_422_get_quiz_questions_empty_payload(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()