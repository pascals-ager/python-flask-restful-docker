from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, make_response, current_app
from flask_restful import Api, Resource
import jwt

from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models import User


api = Blueprint('sign', __name__, url_prefix='/api')
api_wrap = Api(api)

@api.route("/sign",  methods=['GET'])
def sign():
    '''
    In - Request header with user email and password
    Out - A jwt token is sent if the user is active, else an appropriate error message is sent.
    
    '''
    SECRET_KEY = current_app.config['SECRET_KEY']
    email = request.headers.get('email')
    password = request.headers.get('password')
    user = User.query.filter_by(email=email).scalar()
    if user is None:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="User does not exist"'})  
    elif not check_password_hash(user.password,password):
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Incorrect Password"'})
    elif not user.confirmed:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Missing User Confirmation"'})
    else:
        token = jwt.encode({'public_id' : user.email,
         'exp' : datetime.utcnow() + timedelta(minutes=30)},
          SECRET_KEY,
          algorithm='HS256')   #secret key
        return jsonify({'token' : token.decode('UTF-8')})