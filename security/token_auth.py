from functools import wraps
from flask import request, jsonify
from models import User
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            #print(request.headers)
            token = request.headers['Authorization'].split(" ")[1]
            #print(token)

        if not token:
            #print(request.authorization)
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, 'thisisdevsecret')
            #print(data)
            current_user = User.query.filter_by(email=data['public_id']).scalar()
        except Exception as e:
            
            #print(e)
            return jsonify({'message' : str(e) }), 401

        return f(current_user, *args, **kwargs)

    return decorated