import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash
from playhouse.shortcuts import model_to_dict

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

        created_user_dict = model_to_dict(created_user)
        created_user_dict.pop('password')

        return jsonify(
            data=created_user_dict,
            message='Successfully registered user',
            status=201
        ), 201
