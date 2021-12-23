import models


from flask import Blueprint, request, jsonify


from playhouse.shortcuts import model_to_dict

from flask_login import current_user


workouts = Blueprint('workouts', 'workouts')


@workouts.route('/', methods=['GET'])
def workouts_index():
    result = models.Workout.select()

    workout_dicts = [model_to_dict(workout) for workout in result]

    for workout_dict in workout_dicts:
        workout_dict['user'].pop('password')

    return jsonify({
        'data': workout_dicts,
        'message': f"successfully found {len(workout_dicts)} workouts",
        'status': 200
    }), 200


@workouts.route('/', methods=['POST'])
def create_workout():
    payload = request.get_json()
    new_workout = models.Workout.create(name=payload['name'], user=current_user.id)

    workout_dict = model_to_dict(new_workout)

    return jsonify(
        data=workout_dict,
        message='Successfully created the workout',
        status=201
    ), 201


@workouts.route('/<id>', methods=['GET'])
def get_one_workout(id):
    workout = models.Workout.get_by_id(id)

    return jsonify(
        data=model_to_dict(workout),
        message='Successfully found Workout',
        status=200
    ), 200


@workouts.route('/<id>', methods=['DELETE'])
def delete_lift(id):
    delete_query = models.Workout.delete().where(models.Workout.id == id)
    nums_of_rows_deleted = delete_query.execute()

    return jsonify(
        data={},
        message=f"Successfully deleted {nums_of_rows_deleted} workout with id {id}",
        status=200
    ), 200
