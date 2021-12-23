from flask import Flask, jsonify


from resources.workouts import workouts
from resources.lifts import lifts
from resources.users import users



import models



from flask_cors import CORS
from flask_login import LoginManager

import os


DEBUG=True
PORT=8000



app = Flask(__name__)


app.secret_key = 'poopbuttmcgee'
login_manager = LoginManager()
login_manager.init_app(app)


CORS(app, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(workouts, url_prefix='/api/v1/workouts/')
app.register_blueprint(lifts, url_prefix='/api/v1/lifts/')
app.register_blueprint(users, url_prefix='/api/v1/users/')


















if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
