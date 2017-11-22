from datetime import datetime
from flask import Blueprint, request, url_for
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
    email = request.headers.get('email')
    password = request.headers.get('password')
    user = User.query.filter_by(email=email).scalar()
    if user and user.confirmed_on:
        return "The user already exists. Please sign in to use the APIs."
    elif user and not user.confirmed_on:
        return "The user already exists. Please confirm your email and sign-in."
    hashed_password = generate_password_hash(password, method='sha256')
    
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    token = ts.dumps(email, salt="thisisdevsecret")  #secret key

    confirm_url = url_for(
        'register.confirm',
        token=token,
        _external=True)
    return confirm_url

@api.route("/confirm/<token>",  methods=['GET'])
def confirm(token):
    print(token)
    email = ts.loads(token, salt="thisisdevsecret", max_age=86400)  #secret key
    user = User.query.filter_by(email=email).first_or_404()
    user.confirmed=1
    user.confirmed_on=datetime.utcnow()
    db.session.merge(user)
    db.session.commit()
    return "User "+email+" is now confirmed. You may sign-in to use the APIs."
