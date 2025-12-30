from flask import Blueprint, abort, render_template, request, flash, redirect, url_for, Response
from flask_login import login_required, current_user
from model.models import User, UserToChat, Chat
from model.db import db

chat = Blueprint("chat", __name__, template_folder="templates")

@chat.route("/chats/<email>")
@login_required
def myChat(email):
    if email != current_user.email:
        flash("You are not authorized to access this chat.", "error")
        return abort(403)
    
    # Get chats involving the current user
    user_chat_records = UserToChat.query.filter_by(user_id=current_user.id).all()
    chats_data = []
    
    for record in user_chat_records:
        chat = record.chat
        other_user_record = UserToChat.query.filter(
            UserToChat.chat_id == chat.id,
            UserToChat.user_id != current_user.id
        ).first()
        other_user = other_user_record.user if other_user_record else None
        
        chats_data.append({
            'chat': chat,
            'other_user': other_user
        })
    
    return render_template("chats/chat.html", email=current_user.email, chats=chats_data) 

@chat.route("/search-users", methods=["GET", "POST"])  
@login_required
def searchUser():
    searchDone = False  
    searchQuery = ""    
    results = []        
    
    if request.method == "POST":
        searchQuery = request.form.get("search_query", "")
        searchDone = True
        email = User.query.filter(User.email.ilike(f"%{searchQuery}%")).all()
        username = User.query.filter(User.username.ilike(f"%{searchQuery}%")).all()
        results = set(email + username)
        if current_user in results:
            results.remove(current_user)
 
    user_chat_records = UserToChat.query.filter_by(user_id=current_user.id).all()
    chats_data = []
    
    for record in user_chat_records:
        chat = record.chat
        other_user_record = UserToChat.query.filter(
            UserToChat.chat_id == chat.id,
            UserToChat.user_id != current_user.id
        ).first()
        other_user = other_user_record.user if other_user_record else None
        
        chats_data.append({
            'chat': chat,
            'other_user': other_user
        })
    
    return render_template(
        "chats/chat.html", 
        email=current_user.email,
        search_results=results,
        search_performed=searchDone,
        search_query=searchQuery,
        chats=chats_data  
    )

@chat.route("/create-chat/<int:user_id>")
@login_required
def createChat(user_id):
    user = User.query.get(user_id)
    with open("app\static\img\default-chat.jpg", "rb") as f:
        imgByte = f.read()
    newChat = Chat(chat_name=f"Chat with {user.username}", chat_image=imgByte)
    
    db.session.add(newChat)
    db.session.commit()
    userToChat1 = UserToChat(user_id=current_user.id, chat_id=newChat.id)
    userToChat2 = UserToChat(user_id=user.id, chat_id=newChat.id)
    db.session.add(userToChat1)
    db.session.add(userToChat2)
    db.session.commit()
    
    flash("Chat created successfully!", "success")
    return redirect(url_for('chat.myChat', email=current_user.email))

@chat.route('/chat/image/<int:chat_id>')
def chat_image(chat_id):
    chat_obj = Chat.query.get_or_404(chat_id)
    
    if not chat_obj.chat_image:
        return "", 404
    
    return Response(chat_obj.chat_image, mimetype="image/jpeg")

@chat.route("/chat/<int:chat_id>")
@login_required
def viewChat(chat_id):
    chat_obj = Chat.query.get_or_404(chat_id)
    
    user_in_chat = UserToChat.query.filter_by(
        user_id=current_user.id,
        chat_id=chat_id
    ).first()
    
    if not user_in_chat:
        flash("You are not authorized to view this chat.", "danger")
        return abort(403)
    
    other_user_record = UserToChat.query.filter(
        UserToChat.chat_id == chat_id,
        UserToChat.user_id != current_user.id
    ).first()
    other_user = other_user_record.user if other_user_record else None
    
    # messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp).all()
    
    return render_template("chats/chatView.html", 
                         chat=chat_obj, 
                         other_user=other_user)