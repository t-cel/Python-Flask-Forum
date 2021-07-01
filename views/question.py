from flask import jsonify, render_template, request, url_for, redirect, flash, Blueprint
from flask_login import current_user
from flask_login import login_required
import datetime

from models import User, Category, Post, Question, Answer, Vote, db
import views.utils as utils

question_blueprint =  Blueprint('question_blueprint', __name__)

@question_blueprint.route("/question/")
def question():
    question = db.session.query(Question).filter_by(id = int(request.args.get('question_id'))).first()
    answers = db.session.query(Answer).filter_by(question_id = question.id)

    question_data = utils.get_questions_data([question])[0]
    answers_data = utils.get_answers_data(answers)

    data = utils.get_base_data()
    data['question_data'] = question_data
    data['answers_data'] = answers_data
    data['category'] = db.session.query(Category).filter_by(id = question.category_id).first()
    data['has_best'] = answers.filter_by(is_best=True).first() != None

    # parameter from profile page to automatically hover over selected answer
    if 'answer_id' in request.args:
        answer_id = int(request.args.get('answer_id'))
        data['answer_id'] = answer_id

    return render_template(
        'question.html', 
        data = data
    )


@question_blueprint.route("/question/", methods=['POST'])
def question_post():
    question_id = int(request.form.get('question_id'))
    content = request.form.get('answer')

    if not content:
        flash('Answer cannot be empty.', 'error')
        return redirect(url_for('question_blueprint.question', question_id=question_id))

    answer = Answer()
    answer.question_id = question_id
    answer.is_best = False
    answer.author_id = current_user.id
    answer.content = content
    answer.date = datetime.datetime.now()

    db.session.add(answer)       
    db.session.commit()

    flash('Successfully added new answer.', 'info')
    return redirect(url_for('question_blueprint.question', question_id=question_id))


@question_blueprint.route("/vote")
@login_required
def vote():
    post_id = request.args.get('post_id')
    is_up = request.args.get('up') == '1'

    # check if its not current user post
    post = Post.query.filter_by(id=post_id).first()
    if post.author_id == current_user.id:
        return jsonify(result="#1")

    # check if user voted this post earlier
    vote = Vote.query.filter_by(post_id=post_id, author_id=current_user.id).first()
    if vote:
        return jsonify(result="#2")

    vote = Vote()
    vote.post_id = post_id
    vote.author_id = current_user.id
    vote.is_up = is_up

    db.session.add(vote)       
    db.session.commit()

    votes_up = post.votes.filter_by(is_up = True).count()
    votes_down = post.votes.filter_by(is_up = False).count()
    votes_sum = votes_up - votes_down

    return jsonify(result=votes_sum)


@question_blueprint.route("/mark_best")
def mark_best():
    answer_id = request.args.get('answer_id')

    answer = Answer.query.filter_by(id=answer_id).first()
    answer.is_best = True

    db.session.commit()

    flash('Successfully marked answer as best.', 'info')
    return redirect(url_for('question_blueprint.question', question_id=answer.question_id))
