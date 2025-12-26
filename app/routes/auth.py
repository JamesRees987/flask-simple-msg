from flask import Blueprint, render_template, request, flash, redirect, url_for
from model.db import db
from model.models import UserCreds, User
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user

auth = Blueprint("auth", __name__, template_folder="templates")

@auth.route("/signUp", methods=['GET', 'POST'])
def signUp():
    username = request.form.get('username')
    email = request.form.get('email')
    logging.info(f"SignUp attempt for username: {username}, email: {email}")

    if request.method == 'POST':
        password = request.form.get('password')
        password = generate_password_hash(password)

        if password and username and email:
            existing_user = UserCreds.query.filter_by(email=email).first()
            if existing_user:
                logging.warning(f"SignUp failed: Email {email} already registered.")
                flash("Email already registered.", "error")
                return redirect(url_for("auth.signUp"))
            else:
                with open("static\img\default-profile.jpg", "rb") as f:
                    imgByte = f.read()

                user = UserCreds(username=username, password_hash=password, email=email, profile_image=imgByte)
                db.session.add(user)
                db.session.commit()
                logging.info(f"User {username} successfully registered.")
                flash("Registration successful! Please sign in.", "success")
                return redirect(url_for("auth.signIn"))

    return render_template("auth/signUp.html")

@auth.route("/signIn", methods=['GET', 'POST'])
def signIn():
    if current_user.is_authenticated:
        return redirect(url_for('route.home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('route.home'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template("auth/signIn.html")  

@auth.route("/signIn/recover")
def recover():
    return render_template("auth/recover.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.signIn'))