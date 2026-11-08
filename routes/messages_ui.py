from flask import Blueprint, render_template

messages_bp = Blueprint("messages_ui", __name__)


@messages_bp.route("/messages")
def messages_page():
    return render_template("messages.html")
