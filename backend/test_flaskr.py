import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation
    and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["categories"]))

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["categories"]))

    def test_create_questions(self):
        data = {
            "question": "qqq",
            "answer": "aaa",
            "category": 1,
            "difficulty": 1,
        }
        res = self.client().post(
            "/questions",
            data=json.dumps(data),
            content_type="application/json",
        )
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data["id"])
        self.assertEqual(data["question"], "qqq")
        self.assertEqual(data["answer"], "aaa")
        self.assertEqual(data["category"], 1)
        self.assertEqual(data["difficulty"], 1)

    def test_create_questions_failure(self):
        data = {
            "question": "qqq",
            "answer": "aaa",
            "category": "xxx",
            "difficulty": 1,
        }
        res = self.client().post(
            "/questions",
            data=json.dumps(data),
            content_type="application/json",
        )
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)

    def test_delete_questions(self):
        data = {
            "question": "qqq",
            "answer": "aaa",
            "category": 1,
            "difficulty": 1,
        }
        res = self.client().post(
            "/questions",
            data=json.dumps(data),
            content_type="application/json",
        )
        data = json.loads(res.data)
        question_id = data["id"]

        res = self.client().delete(f"/questions/{question_id}")
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertEqual(data["id"], question_id)
        self.assertEqual(data["question"], "qqq")
        self.assertEqual(data["answer"], "aaa")
        self.assertEqual(data["category"], 1)
        self.assertEqual(data["difficulty"], 1)

    def test_delete_questions_failure(self):
        data = {
            "question": "qqq",
            "answer": "aaa",
            "category": 1,
            "difficulty": 1,
        }
        res = self.client().post(
            "/questions",
            data=json.dumps(data),
            content_type="application/json",
        )
        data = json.loads(res.data)
        question_id = data["id"]

        res = self.client().delete(f"/questions/{question_id + 1}")
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    def test_search_questions(self):
        data = {"search_term": "title"}
        res = self.client().post(
            "/questions/search",
            data=json.dumps(data),
            content_type="application/json",
        )
        data = json.loads(res.data)

        self.assertEqual(data["total_questions"], 2)

    def test_search_questions_failure(self):
        data = {"search_term": "-------------"}
        res = self.client().post(
            "/questions/search",
            data=json.dumps(data),
            content_type="application/json",
        )
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    def test_get_questions_by_category(self):
        category = 4
        res = self.client().get(f"/categories/{category}/questions")
        data = json.loads(res.data)

        self.assertEqual(data["total_questions"], 4)

    def test_get_questions_by_category_failure(self):
        category = 1000
        res = self.client().get(f"/categories/{category}/questions")
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    def test_get_quizzes(self):
        category = {"id": 4, "type": "hoge"}
        previous_questions = []
        for _ in range(4):
            data = {
                "previous_questions": previous_questions,
                "quiz_category": category,
            }
            res = self.client().post(
                "/quizzes",
                data=json.dumps(data),
                content_type="application/json",
            )
            data = json.loads(res.data)
            self.assertTrue(data["success"])
            previous_questions.append(data["question"]["question"])
        data = {
            "previous_questions": previous_questions,
            "quiz_category": category,
        }
        res = self.client().post(
            f"/quizzes", data=json.dumps(data), content_type="application/json"
        )
        data = json.loads(res.data)
        self.assertFalse(data["success"])

    def test_get_quizzes_failure(self):
        category = {"id": 1000, "type": "hoge"}
        data = {"previous_questions": [], "quiz_category": category}
        res = self.client().post(
            "/quizzes", data=json.dumps(data), content_type="application/json"
        )
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
