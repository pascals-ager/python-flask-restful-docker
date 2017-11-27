from datetime import datetime
from flask import Blueprint, request, url_for, current_app, jsonify, make_response
from flask_restful import Api, Resource

from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models import User

from itsdangerous import URLSafeTimedSerializer
ts = URLSafeTimedSerializer('thisisdevsecret')   #secret key

api = Blueprint('register', __name__, url_prefix='/api')
api_wrap = Api(api)

@api.route("/signup",  methods=['POST'])
def signup():
    '''
    In  - Request header with user email and password
    Out - Confirmation link for user activation

    The confirmation link consists of a serialized token which is used to identify the user
    '''

    email = request.headers.get('email')
    password = request.headers.get('password')
    SALT_KEY = current_app.config['SALT_KEY']

    try:
        user = User.query.filter_by(email=email).scalar()
    except Exception as e:
        return make_response(str(e).split('\n')[0], 401, {'WWW-Authenticate' : 'Issue occured while querying the database'})
    
    if user and user.confirmed_on:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="The email is already in use"'})
    elif user and not user.confirmed_on:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="The email is registered but is unconfirmed"'})
    hashed_password = generate_password_hash(password, method='sha256')
    
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    token = ts.dumps(email, salt=SALT_KEY)  #salt key

    confirm_url = url_for(
        'register.confirm',
        token=token,
        _external=True)
    return jsonify({'confirmation_url': confirm_url})

@api.route("/confirm/<token>",  methods=['GET'])
def confirm(token):
    '''
    In - Request with token parameter
    Out- User activation message

    '''
    SALT_KEY = current_app.config['SALT_KEY']
    email = ts.loads(token, salt=SALT_KEY, max_age=86400)  #salt key
    user = User.query.filter_by(email=email).first_or_404()
    user.confirmed=1
    user.confirmed_on=datetime.utcnow()
    db.session.merge(user)
    db.session.commit()
    return jsonify({'confirmation_message': 'User '+ email +' is confirmed'})
