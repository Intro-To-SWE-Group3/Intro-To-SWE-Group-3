# app.py
# Main Flask application entry point.
# Creates and configures the Flask app, registers all API routes,
# enables any shared settings such as CORS, and starts the backend server.

import flask
from dotenv import load_dotenv

load_dotenv(override=True)

from routes.listings import app as listings_blueprint
# Connect the homepage routes to the Flask app.
from routes.homepage import app as homepage_blueprint

app = flask.Flask(__name__)
app.register_blueprint(listings_blueprint)
# Register the homepage routes with the Flask app.
app.register_blueprint(homepage_blueprint)

from flask_cors import CORS
CORS(app)



# When someone visits the site's home page using a GET request,
# Flask runs the homepage function below. 
@app.route("/", methods=["GET"])
def homepage():
    return flask.render_template("index.html")

@app.route("/create", methods=["GET"])
def create_listing():
    return flask.render_template("create.html")

if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True, host='127.0.0.1', port=5000)