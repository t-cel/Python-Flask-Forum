from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask import render_template, Blueprint, current_app, request, redirect, url_for, flash

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

import views.utils as utils
from models import User, Category, Post, Question, Answer, Vote, db

import os, glob

edit_profile_blueprint =  Blueprint('edit_profile_blueprint', __name__)

ALLOWED_EXTENSIONS = {'jpg'}

@edit_profile_blueprint.route("/edit_profile/")
@login_required
def edit_profile():
    return render_template('edit_profile.html', data=utils.get_base_data())

@edit_profile_blueprint.route("/edit_profile/", methods=['POST'])
@login_required
def edit_profile_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    description = request.form.get('description')

    if name: current_user.name = name
    
    if email:
        if User.query.filter_by(email=email).first():
            flash('User with this email already exists, choose different email.', 'error')
            return redirect(url_for('edit_profile_blueprint.edit_profile'))
        current_user.email = email
    
    if password: current_user.password = generate_password_hash(password)
    if description: current_user.description = description

    db.session.commit()

    picture = request.files['profile_picture']
    if picture and picture.filename:
        if not allowed_file(picture.filename):
            flash('Only .jpg images are supported.', 'error')
            return redirect(url_for('edit_profile_blueprint.edit_profile'))

        # remove old picture
        for filename in glob.glob(f"{current_app.config['UPLOAD_FOLDER']}/{current_user.id}.*"):
            os.remove(filename) 

        # save new picture
        filename = secure_filename(picture.filename)
        picture.save(f"{current_app.config['UPLOAD_FOLDER']}/{current_user.id}.{get_extension(filename)}")

    
    flash('Changes successfully applied.', 'info')
    return redirect(url_for('user_profile_blueprint.user_profile', user_id=current_user.id))


def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower() 


def allowed_file(filename):
    """
        Checks whether filename has allowed extension
    """
    return '.' in filename and \
           get_extension(filename) in ALLOWED_EXTENSIONS

