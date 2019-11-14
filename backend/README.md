# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Endpoints

Endpoints
- GET '/categories'
- GET '/questions'
- POST '/questions'
- DELETE '/questions'

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, an integer category id, and a single value, a category type.
{1 : "Science",
 2 : "Art",
 3 : "Geography",
 4 : "History",
 5 : "Entertainment",
 6 : "Sports"}

### GET '/questions'
- Fetches a dictionary of questions which includes a slice of questions which are shown in one page, the total number of questions, the current category and a full of the full categories.
- Request Arguments: None
- Returns: An object with six keys, a success flag, a question id, a question text, an answer text, a category id and a difficulty score.
{'success' : a success flag,
'questions' : upto ten questions in one page,
'total_questions' : the total number of questions in the DB,
'current_category' : the current category,
'categories' : a dictionary of the categories (see GET '/categories')}

### POST '/questions'
- Post a dictionary of a question to create a new question entry.
- Request Arguments: An object with four keys, a question text, an answer text, a category id and a difficulty score.
{
    "question": question,
    "answer": answer,
    "category": category id (integer),
    "difficulty": difficulty score,
}
- Returns: An object with six keys, which corresponds to the newly created question.
{'success' : True,
'id' : 4,
'question' : a question,
'answer' : the corresponding answer to the question,
'category' : category id (integer),
'difficulty' : difficulty score}

### DELETE '/questions/<int:question_id>'
- Delete a question specified given id.
- Request Arguments: None
- Returns: An object with six keys, which corresponds to the deleted question.
{'success' : True,
'id' : 4,
'question' : a question,
'answer' : the corresponding answer to the question,
'category' : category id (integer),
'difficulty' : difficulty score}


### POST '/questions/search'
- Fetches questions which includes the given search term as a substring.
- Request Arguments: 
{'search_term': search term string}
- Returns: An object with three keys, questions, total_questions, current_categories.
{
 "questions": questions that match the search term,
 "total_questions": the total number of questions returned,
 "current_category": the current category}

### GET '/categories/<int:category>/questions'
- Fetches questions which have the given category id.
- Request Arguments: None
- Returns: An object with three keys, questions, total_questions, current_categories.
{
 "questions": questions that have the given category id,
 "total_questions": the total number of questions returned,
 "current_category": the current category}

### POST '/quizzed'
- Fetches questions to play the quiz, which are fetched one by one from the questions specified by the given category id.
- Request Arguments: 
{
 "previous_questions": questions which are previously shown
 "quiz_category": category id which specifies the whole quiz set}
- Returns: An object with two keys, success, question.
{
 "success": success flag,
 "question": a question sampled from the whole quiz set}


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```