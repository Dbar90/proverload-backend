import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user

users = Blueprint('users', 'users')

@users.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()

    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(
            data={},
            message='A use with that email already exists',
            status=401
        ), 401

    except models.DoesNotExist:
        pw_hash = generate_password_hash(payload['password'])
        created_user = models.User.create(
            email=payload['email'],
            password=pw_hash
        )

        login_user(created_user)

        created_user_dict = model_to_dict(created_user)
        created_user_dict.pop('password')

        return jsonify(
            data=created_user_dict,
            message='Successfully registered user',
            status=201
        ), 201

@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()

    try:
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)

        password_is_good = check_password_hash(user_dict['password'], payload['password'])
        if (password_is_good):
            login_user(user)
            user_dict.pop('password')

            return jsonify(
                data=user_dict,
                message=f"Successfully logged in {user_dict['email']}",
                status=200
            ), 200
        else:
            return jsonify(
                data={},
                message="Email or password is incorrect",
                status=401
            ), 401

    except models.DoesNotExist:
        return jsonify(
            data={},
            message="Email or password is incorrect", 
            status=401
        ), 401
