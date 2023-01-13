from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#Initialize the db
db = SQLAlchemy()

def create_app():

    #Initialize the app
    app = Flask(__name__)

    #Configs
    app.config['SECRET_KEY'] = '123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' 
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))
     
    from . import models
    with app.app_context():
        db.create_all()

    #Blueprint for Auth parts
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #Bluprint for non-Auth parts
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

     

