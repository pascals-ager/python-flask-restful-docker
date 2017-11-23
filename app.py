import os
from datetime import datetime

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy

from models import User
import config

from extensions import db
from api import registerApi,signApi,serviceApi


def create_app(config_name):
    config_object = ".".join(('config',config_name))
    app = Flask(__name__)
    app.config.from_object(config_object)

    
    db.init_app(app)

    
    app.register_blueprint(registerApi)    
    app.register_blueprint(signApi)
    app.register_blueprint(serviceApi)

    return app


def init_db():
    with current_app.context():
        db.create_all()




if __name__=='__main__':    
    app = create_app(os.environ['ENV_SETTINGS'])

    app.run(debug=True)
