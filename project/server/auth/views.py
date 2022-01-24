from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from importlib_metadata import email

from project.server import bcrypt, db
from project.server.models import User

auth_blueprint = Blueprint('auth', __name__)

class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def get(self):
        responseObject = {
            'status': 'success',
            'message': 'Request successful but please send an HTTP POST request to register the user.'
        }
        return make_response(jsonify(responseObject)), 201

    def post(self):
        # get the post data
        post_data = request.get_json()
        print(request)
        # print(post_data)
        # print('the email is ' + post_data.get('email'))
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        print(user)
        if not user:
            print('no user')
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )
                print('inserting user')
                # insert the user
                db.session.add(user)
                db.session.commit()
                print('this worked')
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                print('generated token: ')
                print(type(auth_token))
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                    # 'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                print('the exception is ' + str(e))
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202


# define the API resources
registration_view = RegisterAPI.as_view('register_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST', 'GET']
)