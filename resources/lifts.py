import models


from flask import Blueprint, request, jsonify


from playhouse.shortcuts import model_to_dict


lifts = Blueprint('lifts', 'lifts')





@lifts.route('/', methods=['GET'])
def lifts_index():
    result = models.Lift.select()

    lift_dicts = [model_to_dict(lift) for lift in result]

    return jsonify({
        'data': lift_dicts,
        'message': f"successfully found {len(lift_dicts)} lifts",
        'status': 200
    }), 200


@lifts.route('/', methods=['POST'])
def create_lift():
    payload = request.get_json()
    new_lift = models.Lift.create(name=payload['name'], start_weight=payload['start_weight'], current_weight=payload['current_weight'], sets=payload['sets'], reps=payload['reps'], personal_best=payload['personal_best'], notes=payload['notes'])

    lift_dict = model_to_dict(new_lift)

    return jsonify(
        data=lift_dict,
        message='Successfully created the lift',
        status=201
    ), 201
