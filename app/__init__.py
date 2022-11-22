from flask import Flask
from flask_bootstrap import Bootstrap
from .views import page
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from .models import User, db
from flask_login import LoginManager
from .models import User
from .views import loginManager
from .consts import LOGIN_REQUIRED

app = Flask(__name__)




bootstrap = Bootstrap()
csrf= CSRFProtect()



def create_app(config):
    app.config.from_object(config)
    
    csrf.init_app(app)
    bootstrap.init_app(app)
    loginManager.init_app(app)
    loginManager.login_view='.login'
    loginManager.login_message = LOGIN_REQUIRED
    app.register_blueprint(page)

    with app.app_context():
        db.init_app(app)
        db.create_all()


    return app