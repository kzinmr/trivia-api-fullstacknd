from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db = setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})  # noqa: F841

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def add_cors_headers(response):
        # response.headers.add('Access-Control-Allow-Origin', r)
        # response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        # response.headers.add('Access-Control-Allow-Headers', 'Cache-Control,X-Requested-With')
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,OPTIONS,PATCH,DELETE"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/categories")
    def get_categories():
        categories = db.session.query(Category.id, Category.type).all()
        categories = [type for id, type in categories]
        if len(categories) == 0:
            abort(404)
        else:
            return jsonify({"success": True, "categories": categories})

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions")
    def get_questions():
        page = request.args.get("page", 1, type=int)
        data = (
            db.session.query(Question)
            .order_by(Question.id)
            .slice(page, (page + 1) * 10 + 1)
            .all()
        )
        data = list(data)
        if len(data) == 0:
            abort(404)
        else:
            questions = [q.question for q in data]
            total_questions = len(questions)
            categories = [q.category for q in data]
            current_category = categories[0]  # NOTE: ok?
            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "total_questions": total_questions,
                    "current_category": current_category,
                    "categories": categories,
                }
            )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_questions(question_id):
        error = False
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(404)
        try:
            db.session.delete(question)
            db.session.commit()
            # just for testing
            question = {
                "id": question.id,
                "question": question.question,
                "answer": question.answer,
                "category": question.category,
                "difficulty": question.difficulty,
            }
        except Exception:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        if not error:
            # just for testing
            return jsonify(
                {
                    "success": True,
                    "id": question["id"],
                    "question": question["question"],
                    "answer": question["answer"],
                    "category": question["category"],
                    "difficulty": question["difficulty"],
                }
            )
        else:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route("/questions", methods=["POST"])
    def create_question_submission():
        error = False
        try:
            # Assume that no fields are multi-valued field.
            formdata = {k: v[0] for k, v in request.form.lists()}
            formdata["category"] = int(formdata["category"])
            formdata["difficulty"] = int(formdata["difficulty"])

            question = Question(**formdata)
            db.session.add(question)
            db.session.commit()
            question = {
                "id": question.id,
                "question": question.question,
                "answer": question.answer,
                "category": question.category,
                "difficulty": question.difficulty,
            }
        except Exception:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        if not error:
            return jsonify(
                {
                    "success": True,
                    "id": question["id"],
                    "question": question["question"],
                    "answer": question["answer"],
                    "category": question["category"],
                    "difficulty": question["difficulty"],
                }
            )
        else:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions/search", methods=["POST"])
    def search_questions():

        search_term = request.form.get("search_term", "")
        data = (
            db.session.query(Question)
            .filter(Question.question.ilike(f"%{search_term}%"))
            .all()
        )

        questions = [q.question for q in data]
        total_questions = len(data)
        current_category = data[0].category  # NOTE: ok?
        response = {
            "questions": questions,
            "total_questions": total_questions,
            "current_category": current_category,
        }

        return jsonify(response)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    def __get_questions_by_category(category):
        data = db.session.query(Question).filter(Question.category == category).all()
        return [q.question for q in data]

    @app.route("/categories/<int:category>/questions")
    def get_questions_by_category(category):
        questions = __get_questions_by_category(category)
        total_questions = len(questions)
        response = {
            "questions": questions,
            "total_questions": total_questions,
            "current_category": category,
        }

        return jsonify(response)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=["POST"])
    def get_quizzes():
        previous_questions = [
            v for k, v in request.form.lists() if k == "previous_questions"
        ]
        previous_questions = set(previous_questions[0]) if previous_questions else {}
        quiz_category = int(request.form.get("quiz_category", 0))
        questions = __get_questions_by_category(quiz_category)
        questions = [q for q in questions if q not in previous_questions]
        if len(questions) > 0:
            question = random.sample(questions, 1)[0]
            response = {"success": True, "question": question}
        else:
            response = {"success": False, "question": ""}
        return jsonify(response)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    return app