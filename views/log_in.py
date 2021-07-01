from flask import url_for, render_template, Blueprint, current_app, redirect, request, flash
from flask_login import login_user, logout_user, login_required

from werkzeug.security import check_password_hash

from models import User, db
import views.utils as utils

log_in_blueprint = Blueprint('log_in_blueprint', __name__)

@log_in_blueprint.route("/log_in/")
def log_in():
    return render_template('log_in.html', data=utils.get_base_data())


@log_in_blueprint.route("/log_in/", methods=['POST'])
def log_in_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('home_blueprint.home'))

    flash('Wrong email or password.', 'error')
    return redirect(url_for('log_in_blueprint.log_in'))


@log_in_blueprint.route("/log_out/")
@login_required
def log_out():
    logout_user()
    return redirect(url_for('home_blueprint.home'))