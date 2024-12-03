from flask_sqlalchemy import SQLAlchemy
from flask import Flask
#from app.routes import main

db = SQLAlchemy()
def create_app():
    app = Flask(__name__,template_folder='../templates') #specify templates folder
    app.config.from_object('app.config.Config')
    db.init_app(app)

    with app.app_context():
        from app.models import Customer
        db.create_all()
    from app.routes import main
    app.register_blueprint(main)

    return app
