from flask import Blueprint, request, jsonify
from models import users
from helpers.sendmail import send_email
from routes import api
from config.db_connection import app_configuration
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from helpers.convert_object_ids import convert_model_ids
from http import HTTPStatus
import sys
import logging
import json
from dotenv import load_dotenv
load_dotenv()

_logger = logging.getLogger(__name__)

users_bp = Blueprint('users', __name__)


@users_bp.route(api.route['register_user'], methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def register_user():
    '''
    user registration
    '''
    if request.method == 'POST':
        required_args = ['userName',
                         'password', 'confirmPassword', 'email', 'privilege']
        errors = {}
        if not request.args.get('lang'):
            errors['lang'] = "'lang' is a required parameter"
        for arg in required_args:
            if not request.json.get(arg):
                errors[arg] = f"'{arg}' is a required parameter"
        if errors:
            return jsonify(dict(

                message="please specify one of the following query parameters. Refer to the API documentation for details.",
                errors=errors
            )), 400

        lang = request.args.get('lang').strip()
        user_name = request.json.get('userName').strip()
        email = request.json.get('email')
        password = request.json.get('password').strip().encode("utf-8")
        plain_password = request.json.get('password')
        confirm_password = request.json.get(
            'confirmPassword').strip().encode("utf-8")
        privilege = request.json.get('privilege').strip()

        model = users.User(lang)

        if password != confirm_password:
            return jsonify(
                {
                    "message": "passwords did not match!",
                    "success": False
                }), 400

        hashed_password = model.hash_password(password)
        record = {
            "userName": user_name,
            "email": email,
            "password": hashed_password,
            "privilege": privilege
        }
        # check if user already exist
        user_exist = model.is_user_exist(email)
        if user_exist:
            return ({"message": "user already exist!",
                     "success": False
                     }), 401

        result = model.register_user(record)
        if result:
            # email
            subject = "Welcome to Kilega Platform"
            recipients = email
            sender = app_configuration.MAIL_USERNAME
            body = f"Dear {user_name}, <br /> <br /> Welcome to the Kilega platform. " \
                f"<br /> Your username is: <b>{user_name}</b>" \
                f"<br /> Your temporary password is: <b>{plain_password} </b>" \
                f"<br /> <br /> Please remember to reset your password by visting: http://kilega.net/reset" \
                f"<br /> Follow this link to access the dashboard right now: http://kilega.net/login  " \
                f"<br /><br /> PLEASE DO NOT REPLY TO THIS EMAIL  "\
                f"<br /><br /> If you experience any technical challenges or wish to offer donations, suggestion or partnership, do please contact us at <b>support@kilega.net</b>"

            send_email(subject, sender, recipients, body)

            return ({"message": "user registered successfully",
                     "success": True
                     }), 201
        else:
            return jsonify({'message': "something went wrong", "success": False}), 400
    else:
        return jsonify(
            {
                "message": "Invalid request method. Please refer to the API documentation",
                "success": False
            }), HTTPStatus.METHOD_NOT_ALLOWED


@users_bp.route(api.route['login_user'], methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def login_user():
    """
    User login
    """
    if request.method == 'POST':
        required_args = ['email', 'password']
        errors = {}
        if not request.args.get('lang'):
            error['lang'] = 'is a reuired parameter'
        for arg in required_args:
            if not request.json.get(arg):
                errors[arg] = f"'{arg}' is a required parameter"
        if errors:
            return jsonify(dict(

                message="please specify one of the following query parameters. Refer to the API documentation for details.",
                errors=errors
            )), 400

        email = request.json.get("email", None)
        password = request.json.get("password", None).strip().encode('utf-8')
        lang = request.args.get('lang')

        model = users.User(lang)
        login = model.login_user(email, password)
        if login:
            message = "successfully logged"
            userName = login['userName']
            privilege = login['privilege']
            user_id = str(login['_id'])
            email = login['email']
            access_token = create_access_token(identity=userName)

            return jsonify(message=message, userName=userName, privilege=privilege, id=user_id, email=email, access_token=access_token), HTTPStatus.OK
        else:
            return jsonify({"message": "login failed. invalid email or password", "success": False}), HTTPStatus.UNAUTHORIZED
    else:
        return jsonify(
            {
                "message": "Invalid request method. Please refer to the API documentation",
                "success": False
            }), HTTPStatus.METHOD_NOT_ALLOWED


@users_bp.route(api.route['get_users'], methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@jwt_required()
def get_users():
    '''
    Get all users
    '''
    # current_user = get_jwt_identity()
    if request.method == 'GET':
        required_args = ['lang']
        errors = {}
        for arg in required_args:
            if not request.args.get(arg):
                errors[arg] = f"'{arg}' is a required parameter"
        if errors:
            return jsonify(dict(

                message="please specify one of the following query parameters. Refer to the API documentation for details.",
                errors=errors
            )), HTTPStatus.BAD_REQUEST
        lang = request.args.get('lang')
        model = users.User(lang)

        documents = model.get_users()
        return jsonify({"message": "list of users", "data": documents}), HTTPStatus.OK
    else:
        return jsonify(
            {
                "message": "Invalid request method. Please refer to the API documentation",
                "success": False
            }), HTTPStatus.METHOD_NOT_ALLOWED
