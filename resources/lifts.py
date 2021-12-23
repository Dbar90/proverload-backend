import models


from flask import Blueprint, request, jsonify


from playhouse.shortcuts import model_to_dict


lifts = Blueprint('lifts', 'lifts')





@lifts.route('/workouts/<workout_id>', methods=['GET'])
def lifts_index(workout_id):
    workout = models.Workout.get(models.Workout.id == workout_id)

    lift_dicts = [model_to_dict(lift) for lift in workout.lifts]

    return jsonify({
        'data': lift_dicts,
        'message': f"successfully found {len(lift_dicts)} lifts",
        'status': 200
    }), 200


@lifts.route('/', methods=['POST'])
def create_lift():
    payload = request.get_json()
    new_lift = models.Lift.create(name=payload['name'], start_weight=payload['start_weight'], current_weight=payload['current_weight'], sets=payload['sets'], reps=payload['reps'], personal_best=payload['personal_best'], notes=payload['notes'], workout_id=payload['workout_id'])

    lift_dict = model_to_dict(new_lift)

    return jsonify(
        data=lift_dict,
        message='Successfully created the lift',
        status=201
    ), 201


@lifts.route('/<id>', methods=['GET'])
def get_one_lift(id):
    lift = models.Lift.get_by_id(id)

    return jsonify(
        data=model_to_dict(lift),
        message='Successfully found Lift',
        status=200
    ), 200


@lifts.route('/<id>', methods=['PUT'])
def update_lift(id):
    payload = request.get_json()

    models.Lift.update(**payload).where(models.Lift.id == id).execute()

    return jsonify(
        data=model_to_dict(models.Lift.get_by_id(id)),
        message='Updated successfully',
        status=200
    ), 200


@lifts.route('/<id>', methods=['DELETE'])
def delete_lift(id):
    delete_query = models.Lift.delete().where(models.Lift.id == id)
    nums_of_rows_deleted = delete_query.execute()

    return jsonify(
        data={},
        message=f"Successfully deleted {nums_of_rows_deleted} lift with id {id}",
        status=200
    )
