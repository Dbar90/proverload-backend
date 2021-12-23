from flask import Flask, jsonify, after_this_request


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


app.secret_key = os.environ.get('FLASK_APP_SECRET')
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        user = models.User.get_by_id(user_id)
        return user
    except models.DoesNotExist:
        return None


CORS(app, origins=['http://localhost:3000', 'https://progressiveoverload-frontend.herokuapp.com'], supports_credentials=True)

app.register_blueprint(workouts, url_prefix='/api/v1/workouts/')
app.register_blueprint(lifts, url_prefix='/api/v1/lifts/')
app.register_blueprint(users, url_prefix='/api/v1/users/')


@app.before_request # use this decorator to cause a function to run before reqs
def before_request():

    """Connect to the db before each request"""
    print("you should see this before each request") # optional -- to illustrate that this code runs before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
    models.DATABASE.connect()

    @after_this_request # use this decorator to Executes a function after this request
    def after_request(response):
        """Close the db connetion after each request"""
        print("you should see this after each request") # optional -- to illustrate that this code runs after each request
        models.DATABASE.close()
        return response # go ahead and send response back to client
                      # (in our case this will be some JSON)






# ADD THESE THREE LINES -- because we need to initialize the
# tables in production too!
if os.environ.get('FLASK_ENV') != 'development':
    print('\non heroku!')
    models.initialize()








if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
