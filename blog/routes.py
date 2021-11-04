import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm
import blog.read_face as read_face
from blog.models import User
from blog import app, db, bcrypt
from PIL import Image






@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, full_name=form.full_name.data, email=form.email.data,
                    varsity=form.varsity.data, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


