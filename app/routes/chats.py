from flask import Blueprint, abort, render_template, request, flash
from flask_login import login_required, current_user
from model.models import User

chat = Blueprint("chat", __name__, template_folder="templates")

@chat.route("/chats/<email>")
@login_required
def myChat(email):
    if email != current_user.email:
        flash("You are not authorized to access this chat.", "error")
        return abort(403)

    return render_template("chats/chat.html", email=email)

@chat.route("/search-users", methods=["POST"])
@login_required
def searchUser():
    if request.method == "POST":
        searchQuery =  request.form.get("search_query", "")
        searchDone = True
        email = User.query.filter(User.email.ilike(f"%{searchQuery}%")).all()
        username = User.query.filter(User.username.ilike(f"%{searchQuery}%")).all()
        results = set(email + username)
        if current_user in results:
            results.remove(current_user)
    
    return render_template(
        "chats/chat.html", email=current_user.email,
        search_results=results,
        search_performed=searchDone,
        search_query=searchQuery
    )

@chat.route("/create-chat/<int:user_id>")
@login_required
def createChat(user_id):
    # Create a chat id
    # Link the users to the chat id
    # UserToChat model, chat modekl
    # Chat code - only lets certain peple in
    
    return ""