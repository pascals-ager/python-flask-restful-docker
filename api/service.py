from security import token_required
from flask_restful import Api, Resource
from flask import Blueprint


api = Blueprint('service', __name__, url_prefix='/api')
api_wrap = Api(api)



@api.route("/service",  methods=['GET'])
@token_required
def service(current_user):
    return current_user.email + " is accessing protected service using bearer tokens!"