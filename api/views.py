#from flask import request, url_for
#from itsdangerous import URLSafeTimedSerializer
#from werkzeug.security import generate_password_hash, check_password_hash
#ts = URLSafeTimedSerializer('SECRET_KEY')
#from app import app, db


'''
class User(db.Model):
tablename__ = "users"
id = db.Column(db.Integer, primary_key=True)
email = db.Column(db.String(50), unique=True, nullable=False)
password = db.Column(db.String(80), nullable=False)
created_on = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
confirmed = db.Column(db.Boolean, default=False)
confirmed_on = db.Column(db.DateTime, nullable=True)
'''

from datetime import datetime
from flask import Blueprint, request, url_for
from flask_restful import Api, Resource
from itsdangerous import URLSafeTimedSerializer
ts = URLSafeTimedSerializer('SECRET_KEY')
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models import User


api = Blueprint('api', __name__, url_prefix='/api')
api_wrap = Api(api)

@api.route("/signup",  methods=['POST'])
def signup():
    email = request.headers.get('email')
    password = request.headers.get('password')
    print(email)
    print(password)
    user = User.query.filter_by(email=email).first()
    if user and user.confirmed_on:
        return "The user already exists. Please sign in to use the APIs."
    elif user and not user.confirmed:
        return "The user already exists. Please confirm your email and sign-in."
    hashed_password = generate_password_hash(password, method='sha256')
    
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    token = ts.dumps(email, salt="email-confirm-key")

    confirm_url = url_for(
        'api.confirm',
        token=token,
        _external=True)
    return confirm_url

@api.route("/confirm/<token>",  methods=['GET'])
def confirm(token):
    print(token)
    email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    user = User.query.filter_by(email=email).first_or_404()
    user.confirm=1
    user.confirmed_on=datetime.utcnow()
    db.session.merge(user)
    db.session.commit()
    return "User "+email+" is now confirmed. You may sign-in to use the APIs."
    
##########################################

'''    
    email = request.headers.get('email')
    password = request.headers.get('password')
    print(email)
    print(password)
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    token = ts.dumps(email, salt="email-confirm-key")
    confirm_url = url_for(
        '/v1_0.apis_confirm_user_confirm',
        token=token,
        _external=True)
'''