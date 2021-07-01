from flask import render_template, request, Blueprint

import views.utils as utils
from models import User, Category, Post, Question, Answer, Vote, db

user_profile_blueprint =  Blueprint('user_profile_blueprint', __name__)

@user_profile_blueprint.route("/user_profile/")
def user_profile():
    data = utils.get_base_data()
    data['user_id'] = request.args.get('user_id')
    data['user'] = User.query.filter_by(id=int(data['user_id'])).first()

    answers = Answer.query.filter_by(author_id=int(data['user_id']))
    questions = Question.query.filter_by(author_id=int(data['user_id']))

    data['answers_data'] = utils.get_answers_data(answers)
    data['questions_data'] = utils.get_questions_data(questions)

    return render_template(
        'profile.html',
        data=data
    )
