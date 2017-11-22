import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#import config
#######################################


#######################################

from models import User
import config
def create_app(config_name):
    config_object = ".".join(('config',config_name))
    app = Flask(__name__)
    app.config.from_object(config_object)
    #import apis.views
    from extensions import db
    db.init_app(app)
    from api import registerApi,signApi,serviceApi
    app.register_blueprint(registerApi)    
    app.register_blueprint(signApi)
    app.register_blueprint(serviceApi)
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
    app = create_app(os.environ['ENV_SETTINGS'])

    app.run(debug=True)
