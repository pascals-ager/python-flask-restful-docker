from security import token_required
from flask_restful import Api, Resource
from flask import Blueprint, make_response


api = Blueprint('service', __name__, url_prefix='/api')
api_wrap = Api(api)



@api.route("/service",  methods=['GET'])
@token_required
def service(current_user):
    '''
    In - A request header containing a valid jwt token
    The service can be accessed only if the token is valid

    '''
    return make_response(current_user.email + ' is accessing a protected service', 200)