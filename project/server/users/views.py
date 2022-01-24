from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from importlib_metadata import email

from project.server import bcrypt, db
from project.server.models import User

users_blueprint = Blueprint('users', __name__)

class UsersAPI(MethodView):
    """
    Users Information Resource
    """

    def get(self):
        """
        lists all registered users
        returns a JSON object
        # """
        users = User.query.filter_by().all()
        users_list = [{'admin' : user.admin, 'email': user.email, 'id' : user.id, 'registered_on': user.registered_on.strftime("%a, %d %b %Y %H:%M:%S %Z")} for user in users]

        responseObject = {  
            'users' : users_list
        }
        return make_response(jsonify(responseObject)), 201

# define the API resources
users_view = UsersAPI.as_view('register_api')

# add Rules for API Endpoints
users_blueprint.add_url_rule(
    '/users/index',
    view_func=users_view,
    methods=['GET']
)