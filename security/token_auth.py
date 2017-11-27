from functools import wraps
from flask import request, jsonify, current_app
from models import User
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        '''
        The decorator provides a mechanism to validate the jwt token within a requested service
        In the abscence of a valid token, the decoratee service may not be accessed

        '''
        token = None
        SECRET_KEY = current_app.config['SECRET_KEY']

        if 'Authorization' in request.headers:
            #print(request.headers)
            token = request.headers['Authorization'].split(" ")[1]
            #print(token)

        if not token:
            #print(request.authorization)
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, SECRET_KEY,algorithms='HS256') #secret key
            #print(data)
            current_user = User.query.filter_by(email=data['public_id']).scalar()
        except Exception as e:
            
            #print(e)
            return jsonify({'message' : str(e) }), 401

        return f(current_user, *args, **kwargs)

    return decorated