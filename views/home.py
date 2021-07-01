from flask import render_template, Blueprint, request

from models import User, Category, Post, Question, Answer, Vote, db
import views.utils as utils

home_blueprint =  Blueprint('home_blueprint', __name__)

@home_blueprint.route("/home/", methods=['GET', 'POST'])
def home():
    data = utils.get_base_data()
    categories_data = []
    categories = db.session.query(Category).all()

    for category in categories:
        questions = db.session.query(Question).filter_by(category_id = category.id)
        last_question = questions.order_by(Question.date.desc()).first()
        categories_data.append({
            'category': category,
            'questions_count': questions.count(),
            'last_question': last_question,
            'last_question_author_name': last_question.author.name if last_question else '',
            'last_question_date': last_question.date.strftime('%d/%m/%y, %H:%M') if last_question else ''
        })

    data['categories_data'] = categories_data
    data['mode'] = 'categories'

    return render_template(
        'index.html', 
        data=data
    )


@home_blueprint.route("/category/")
def category(): 
    category = db.session.query(Category).filter_by(id = int(request.args.get('category_id'))).first()
    questions = db.session.query(Question).filter_by(category_id = category.id).order_by(Question.date.desc())

    data = utils.get_base_data()
    data['mode'] = 'questions'
    data['category_name'] = category.name
    data['questions_data'] = utils.get_questions_data(questions)
    data['category'] = category

    return render_template(
        'index.html', 
        data = data
    )