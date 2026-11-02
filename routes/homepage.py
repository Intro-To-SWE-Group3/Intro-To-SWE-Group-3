import flask

app = flask.Blueprint("homepage", __name__)


@app.route("/", methods=["GET"])
def show_homepage():
    return flask.render_template("index.html")