from flask_login import current_user

from models import User, Category, Post, Question, Answer, Vote, db

def get_base_data():
    data = {}
    data['logged_user_id'] = current_user.id if current_user.is_authenticated else -1
    return data


def get_questions_data(questions):
    questions_data = []
    for question in questions:
        votes_up = question.votes.filter_by(is_up = True).count()
        votes_down = question.votes.filter_by(is_up = False).count()
        votes_sum = votes_up - votes_down

        question_answers = Answer.query.filter_by(question_id=question.id)

        questions_data.append({
            'question': question,
            'votes_sum': votes_sum,
            'answers_count': question_answers.count(),
            'author_name': question.author.name,
            'has_best': question_answers.filter_by(is_best=True).first() != None,
            'time': question.date.strftime('%d/%m/%y, %H:%M'),
        })

    return questions_data


def get_answers_data(answers):
    answers_data = []
    for answer in answers:
        votes_up = answer.votes.filter_by(is_up = True).count()
        votes_down = answer.votes.filter_by(is_up = False).count()
        votes_sum = votes_up - votes_down

        answers_data.append({
            'answer': answer,
            'question_title': Question.query.filter_by(id=int(answer.question_id)).first().title,
            'votes_sum': votes_sum,
            'is_best': answer.is_best,
            'time': answer.date.strftime('%d/%m/%y, %H:%M')
        })
    
    return answers_data