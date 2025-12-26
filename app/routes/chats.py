from flask import Blueprint, abort, render_template
from flask_login import login_required, current_user

chat = Blueprint("chat", __name__, template_folder="templates")

@chat.route("/chats/<email>")
@login_required
def myChat(email):
    if email != current_user.email:
        abort(403)

    return render_template("chats/chat.html", email=email)
