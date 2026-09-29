# app.py
# Main Flask application entry point.
# Creates and configures the Flask app, registers all API routes,
# enables any shared settings such as CORS, and starts the backend server.

import flask
from dotenv import load_dotenv

load_dotenv(override=True)

from routes.listings import app as listings_blueprint

app = flask.Flask(__name__)
app.register_blueprint(listings_blueprint)

from flask_cors import CORS
CORS(app)

if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True, host='127.0.0.1', port=5000)

# When someone visits the site's home page using a GET request,
# Flask runs the homepage function below. 
@app.route("/", methods=["GET"])
def homepage():
    return """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>KSU Trade Market</title>
    </head>
    <body>
        <h1>KSU Trade Market</h1>
        <p>A marketplace for useful finds shared by fellow students.</p>
        <h2>Available listings</h2>
        <p>Listings will appear here.</p>
    </body>
    </html>
    """
