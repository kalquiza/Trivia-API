import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# helper function to handle pagination
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    Set up CORS
    Allow '*' for origins
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
            )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS'
            )
        return response

    '''
    GET /categories
    Returns a list of categories, success value, and total number of categories
    '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        selection = Category.query.order_by(Category.id).all()
        categories = {category.id: category.type for category in selection}

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories,
            'total_categories': len(Category.query.all())
        })

    '''
    GET /questions
    Returns a list of questions, success value, number of total questions,
    current category, and categories.
    '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        question_selection = Question.query.order_by(Question.id).all()
        questions = paginate_questions(request, question_selection)

        category_selection = Category.query.order_by(Category.id).all()
        categories = {
            category.id: category.type for category in category_selection
        }

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(Question.query.all()),
            'categories': categories,
            'current_category': None
        })

    '''
    DELETE /question/{question_id}
    Deletes the question of the given ID if it exists. Returns the id of the
    deleted question, success value, total number of questions, and question
    list based on the current page number.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': questions,
                'total_questions': len(Question.query.all())
            })

        except Exception as e:
            abort(422)

    '''
    POST /questions
    Creates a new question using the submitted question, answer, difficulty,
    and category. Returns the id of the created question, success value, total
    number of questions, and list of questions.

    A valid request must contain a question and answer with a non-empty string.
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            body = request.get_json()

            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)

            if new_question == "" or new_answer == "":
                abort(422)

            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty
            )
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except Exception as e:
            abort(422)

    '''
    POST /questions/search
    Returns a list of questions based on a search term, returning any
    questions for whom the search term is a substring of the question. Also
    returns the current category id, success value, and total number of
    questions that match the given search term.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            body = request.get_json()
            search_term = body.get('searchTerm', None)
            search = '%'+search_term+'%'
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike(search)).all()
            questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(questions),
                'current_category': None
            })

        except Exception as e:
            abort(422)

    '''
    GET /categories/{category_id}/questions
    Returns a list of questions for a given category, returning any questions
    for the category id. Also returns current category id, success value, and
    total number of questions in the category.
    '''
    @app.route('/categories/<string:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            category = Category.query.filter(
                Category.id == category_id).one_or_none()

            if category is None:
                abort(404)

            selection = Question.query.order_by(Question.id).filter(
                Question.category == category_id).all()
            questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(questions),
                'current_category': category_id
            })

        except Exception as e:
            abort(404)

    '''
    POST /quizzes
    Takes in a category and a list of previous question ids. Returns a
    question from the specified category that is not within the the list of
    previous question ids, a new list of previous question ids appended with
    the id of the returned question, and a success value.

    If no questions from the category are left the same list of previous
    questions is returned and a question with value null.
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        try:
            body = request.get_json()
            quiz_category = body.get('quiz_category', None).get('id', None)
            previous_questions = body.get('previous_questions', None)

            if quiz_category == 0:
                selection = Question.query.order_by(Question.id).all()
            else:
                selection = Question.query.order_by(Question.id).filter(
                    Question.category == str(int(quiz_category))).all()

            questions = [question.format() for question in selection]
            available_questions = [
                question for question in questions
                if question.get('id', None) not in previous_questions
            ]

            if len(available_questions) != 0:
                question = available_questions.pop(
                    random.randrange(len(available_questions)))
                previous_questions.append(question.get('id', None))
            else:
                question = None

            return jsonify({
                'success': True,
                'question': question,
                'previous_questions': previous_questions
            })

        except Exception as e:
            abort(422)

    '''
    Create error handlers for expected errors
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app
