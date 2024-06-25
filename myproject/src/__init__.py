from flask import Flask
from flask_admin.contrib.sqla import ModelView

from src.config import Config
from src.extensions import db, login_manager,admin
from src.views import main_blueprint,products_blueprint, auth_blueprint
from src.models.user import User
from src.models.products import Prod

BLUEPRINTS = [main_blueprint,products_blueprint, auth_blueprint]



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_blueprints(app)
    with app.app_context():
        db.create_all() 

    return app





def register_extensions(app):

    db.init_app(app)
    login_manager.init_app(app)

    #admin
    admin.init_app(app)
    admin.add_view(ModelView(Prod, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


def register_blueprints(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)
    

def register_commands(app):
    pass