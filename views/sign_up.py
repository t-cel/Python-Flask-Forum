from flask import render_template, Blueprint, current_app, url_for, redirect, request, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash
import datetime
import shutil

from models import User, db
import views.utils as utils

sign_up_blueprint = Blueprint('sign_up_blueprint', __name__)

@sign_up_blueprint.route("/sign_up/")
def sign_up():
    return render_template('sign_up.html', data=utils.get_base_data())


@sign_up_blueprint.route("/sign_up/", methods=['POST'])
def sign_up_post():

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not (name and email and password):
        flash('You must fill all data.', 'error')
        return redirect(url_for('sign_up_blueprint.sign_up'))       

    if User.query.filter_by(email=email).first():
        flash('User with this email already exists, choose different email.', 'error')
        return redirect(url_for('sign_up_blueprint.sign_up'))

    user = User()
    user.email = email
    user.name = name
    user.password = generate_password_hash(password)
    user.join_date = datetime.datetime.now()

    db.session.add(user)       
    db.session.commit()

    login_user(user)

    shutil.copy(f"{current_app.config['UPLOAD_FOLDER']}/unknown.jpg", f"{current_app.config['UPLOAD_FOLDER']}/{user.id}.jpg")

    flash('Successfully created new account, you can now vote, answer questions and ask own.', 'info')
    return redirect(url_for('home_blueprint.home'))