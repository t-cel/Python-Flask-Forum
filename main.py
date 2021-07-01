from flask import Flask
from flask_login import LoginManager

from models import User, db

from views.home import home_blueprint
from views.edit_profile import edit_profile_blueprint
from views.log_in import log_in_blueprint
from views.new_question import new_question_blueprint
from views.profile import user_profile_blueprint
from views.question import question_blueprint
from views.sign_up import sign_up_blueprint

app = Flask(__name__)
app.register_blueprint(home_blueprint)
app.register_blueprint(edit_profile_blueprint)
app.register_blueprint(log_in_blueprint)
app.register_blueprint(new_question_blueprint)
app.register_blueprint(user_profile_blueprint)
app.register_blueprint(question_blueprint)
app.register_blueprint(sign_up_blueprint)

login_manager = LoginManager()

UPLOAD_FOLDER = './static/profiles'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.config['SECRET_KEY'] = '4e5f30da153f0eb63eb46a7c'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)

    login_manager.login_view = 'log_in'
    login_manager.init_app(app)

    db.create_all(app=app)

    # app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    # app.run(debug=True, use_debugger=False, use_reloader=True)
    app.run()