from flask import render_template, request, url_for, redirect, Blueprint, flash
from flask_login import login_required, current_user
import datetime

import views.utils as utils
from models import Category, Question, db

new_question_blueprint =  Blueprint('new_question_blueprint', __name__)


@new_question_blueprint.route("/new_question/")
@login_required
def new_question():
    data = utils.get_base_data()
    data['category_id'] = request.args.get('category_id')
    return render_template('new_question.html', data=data)


@new_question_blueprint.route("/new_question/", methods=['POST'])
@login_required
def new_question_post():

    title = request.form.get('title')
    content = request.form.get('content')

    if not content or not title:
        flash('Content and title cannot be empty.', 'error')
        return redirect(url_for('new_question_blueprint.new_question'))


    question = Question()
    question.author_id = current_user.id
    question.content = content
    question.date = datetime.datetime.now()
    question.title = title
    question.category_id = Category.query.filter_by(name=request.form.get('category_id')).first().id

    db.session.add(question)       
    db.session.commit()

    return redirect(url_for('question_blueprint.question', question_id=question.id))

