import re
from flask_sqlalchemy import SQLAlchemy

from config import SQLALCHEMY_DATABASE_URI
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# Convert a model object to dict
def model2dict(model):
    return {c.name: getattr(model, c.name, None) for c in model.__table__.columns}


# Get survey data
def get_survey_data(survey_id):
    # Survey object
    survey_obj = Survey.query.filter_by(index=survey_id).first()
    # Collect all survey data: questions, options
    question_objs = Question.query.filter_by(survey_id=survey_id).all()
    # Sort questions
    question_objs = sorted(question_objs, key=lambda q: q.question_index)
    # Fetch options for questions
    all_option_objs = []
    for question_obj in question_objs:
        # Question type:
        # 1 for single choice
        # 2 for multiple choice
        # 3 for blank filling
        # 4 for numeric filling
        # 5 for rating
        if question_obj.type < 3:
            option_objs = Option.query.filter_by(question_id=question_obj.index).all()
            option_objs = sorted(option_objs, key=lambda op: op.option_index)
            all_option_objs.append(option_objs)
        else:
            all_option_objs.append([])
    # Convert model to dict
    survey_dict = model2dict(survey_obj)
    question_dicts = [model2dict(question_obj) for question_obj in question_objs]
    all_option_dicts = []
    for i in range(len(all_option_objs)):
        all_option_dicts.append([model2dict(option_obj) for option_obj in all_option_objs[i]])

    return survey_dict, question_dicts, all_option_dicts


# Get submission data
def get_submit_data(survey_id):
    # Submit objects
    submit_objs = Submit.query.filter_by(survey_id=survey_id).all()
    submit_objs = sorted(submit_objs, key=lambda s: s.index)
    # Get answers for each submit
    all_answers = []
    for submit_obj in submit_objs:
        answers = Answer.query.filter_by(submit_id=submit_obj.index).all()
        answers = sorted(answers, key=lambda a: a.index)
        all_answers.append(answers)

    # Transform models to dicts
    submit_dicts = [model2dict(submit_obj) for submit_obj in submit_objs]
    all_answer_dicts = []
    for i in range(len(all_answers)):
        all_answer_dicts.append([model2dict(answer_obj) for answer_obj in all_answers[i]])
        # Excape double quotes
        for answer in all_answer_dicts[-1]:
            answer['content'] = re.sub('"', '`', answer['content'])

    return submit_dicts, all_answer_dicts


class User(db.Model):
    __tablename__ = 'user'
    # User information
    username = db.Column(db.String(40), primary_key=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), unique=True, nullable=False)


class Survey(db.Model):
    __tablename__ = 'survey'
    # Survey information
    index = db.Column(db.INT, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(40), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    # Status of survey: false for unpublished, true for published
    status = db.Column(db.Boolean, nullable=False)
    # Answer type
    # 0 for registered users only
    # positive integer for all users and allowing multiple times in total
    # negative integer for all users and allowing multiple times in a single day
    answer_type = db.Column(db.INT, nullable=False)
    # Last update time
    update_time = db.Column(db.String(20), nullable=False)
    # Publish time
    publish_time = db.Column(db.String(20), nullable=True)


class Question(db.Model):
    __tablename__ = 'question'
    # Question information
    index = db.Column(db.INT, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    # Question type:
    # 1 for single choice
    # 2 for multiple choice
    # 3 for blank filling
    # 4 for numeric filling
    # 5 for rating
    type = db.Column(db.INT, nullable=False)
    # Source survey index
    survey_id = db.Column(db.INT, nullable=False)
    # Index of question in survey
    question_index = db.Column(db.INT, nullable=False)
    # Number of options for choice questions
    num_choices = db.Column(db.INT, nullable=False)
    # Number of minimum choosing for multi-choice questions
    num_min_chosen = db.Column(db.INT, nullable=False)
    # Number of maximum choosing for multi-choice questions
    num_max_chosen = db.Column(db.INT, nullable=False)
    # Row count for blank filling questions
    single_row = db.Column(db.Boolean, nullable=True)
    # Numeric format for number filling questions
    fill_digit = db.Column(db.Boolean, nullable=True)
    # Level count for rate questions
    levels = db.Column(db.INT, nullable=True)
    # Whether this problem is compulsory
    compulsory = db.Column(db.Boolean, nullable=False)


class Option(db.Model):
    __tablename__ = 'option'
    # Option information
    index = db.Column(db.INT, primary_key=True, autoincrement=True)
    question_id = db.Column(db.INT, nullable=False)
    option_index = db.Column(db.INT, nullable=False)
    text = db.Column(db.String(100), nullable=False)


class Submit(db.Model):
    __tablename__ = 'submit'
    # Submit information
    index = db.Column(db.INT, primary_key=True, autoincrement=True)
    survey_id = db.Column(db.INT, nullable=False)
    submit_ip = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(40), nullable=True)
    submit_date = db.Column(db.String(10), nullable=False)


class Answer(db.Model):
    __tablename__ = 'answer'
    # Answer information
    index = db.Column(db.INT, primary_key=True, autoincrement=True)
    question_id = db.Column(db.INT, nullable=False)
    submit_id = db.Column(db.INT, nullable=False)
    survey_id = db.Column(db.INT, nullable=False)
    type = db.Column(db.INT, nullable=False)
    content = db.Column(db.String(200), nullable=False)
