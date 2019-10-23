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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()