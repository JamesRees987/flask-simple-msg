from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import Response, request, redirect, url_for, flash
from model.db import db
from model.models import User

route = Blueprint("route", __name__, template_folder="templates")

@route.route("/")
@route.route("/home")
def home():
    return render_template("home.html")

@route.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@route.route('/upload-profile-image', methods=['POST', 'GET'])
@login_required
def upload_profile_image():
    if 'profile_image' not in request.files:
        flash('No file selected', 'danger')
        return redirect(url_for('route.settings'))
    
    file = request.files['profile_image']
    
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('route.settings'))
    
    image_data = file.read()
    
    if len(image_data) > 5 * 1024 * 1024:
        flash('File size exceeds 5MB limit', 'danger')
        return redirect(url_for('route.settings'))
    
    current_user.profile_image = image_data
    db.session.commit()
    
    flash('Profile picture updated successfully!', 'success')
    return redirect(url_for('route.settings'))

@route.route("/profile/image", methods=['POST', 'GET'])
@route.route("/profile/image/<int:user_id>", methods=['POST', 'GET'])
@login_required
def profile_image(user_id=None):
    if user_id:
        user = User.query.get(user_id)
        print(user)
        if not user or not user.profile_image:
            return "", 404
        return Response(user.profile_image, mimetype="image/jpeg")
    
    if not current_user.profile_image:
        return "", 404
    
    return Response(current_user.profile_image, mimetype="image/jpeg")





