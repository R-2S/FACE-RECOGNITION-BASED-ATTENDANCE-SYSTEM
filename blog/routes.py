import os
import secrets # generate random digit
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required  # Current User Status
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm   # Import Forms
import blog.read_face as read_face  # Import Face Recognition Module
from blog.models import user   # Import User part
from blog import app, db, bcrypt    # db, byrcrp for encryption
from PIL import Image  # Image upload / converting etc.


@app.route("/")
def home():
    courses = [
        {'code': 'CSE 410', 'title': 'Software Development'},
        {'code': 'CSE 427', 'title': 'Machine Learning'}
    ]

    return render_template('home.html', courses=courses)


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


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid Credentials', 'danger')
    
    return render_template('login.html', title='Login', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (1000, 1000)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture1.data:
            picture_file1 = save_picture(form.picture1.data)
            current_user.image_file1 = picture_file1
        
        if form.picture2.data:
            picture_file2 = save_picture(form.picture2.data)
            current_user.image_file2 = picture_file2
        
        if form.picture3.data:
            picture_file3 = save_picture(form.picture3.data)
            current_user.image_file3 = picture_file3
        
        current_user.username = form.username.data
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.varsity = form.varsity.data
        db.session.commit()
        
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email
        form.varsity.data = current_user.varsity
    
    image_file1 = url_for('static', filename='profile_pics/' + current_user.image_file1)
    image_file2 = url_for('static', filename='profile_pics/' + current_user.image_file2)
    image_file3 = url_for('static', filename='profile_pics/' + current_user.image_file3)
    
    return render_template('profile.html', title='Profile', image_file1=image_file1,
                            image_file2=image_file2, image_file3=image_file3, form=form)


@app.route("/attendance", methods=['GET', 'POST'])
@login_required
def attendance():
    return render_template('attendance.html', title='Attendance')


@app.route("/face", methods=['GET', 'POST'])
@login_required
def face():
    read_face.face_checker()
    return render_template('processed.html', title='Face Cheker')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
