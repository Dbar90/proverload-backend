from flask import Flask, jsonify


# from resources.workouts import workouts
from resources.lifts import lifts
# from resources.users import users


import models


DEBUG=True
PORT=8000

app = Flask(__name__)


# app.register_blueprint(workouts, url_prefix='/api/v1/proverload')
app.register_blueprint(lifts, url_prefix='/api/v1/lifts')
# app.register_blueprint(users, url_prefix='/api/v1/users')


















if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
