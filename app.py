import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#import config
#######################################


#######################################

from models import User
import config
def create_app():
    app = Flask(__name__)
    app.config.from_object(config.DevelopmentConfig)
    #import apis.views
    from extensions import db
    db.init_app(app)
    from api import api
    app.register_blueprint(api)
    with app.app_context():
        db.create_all()
    
    return app


#######################################

'''def create_app(config_name):
    config_object = ".".join(('config',config_name))
    app = Flask(__name__)     
    app.config.from_object(config_object)
    db.init_app(app)
    return app'''

#######################################





if __name__=='__main__':    
    app=create_app()

    app.run(debug=True)
