from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Registration No.', validators=[DataRequired(), Length(min=6, max=10)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=4, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    varsity = StringField('University', validators=[DataRequired(), Length(min=2, max=60)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Registration No.', validators=[DataRequired(), Length(min=6, max=10)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=4, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    varsity = StringField('University', validators=[DataRequired(), Length(min=2, max=60)])
    picture1 = FileField('Update Profile 1', validators=[FileAllowed(['jpg', 'png'])])
    picture2 = FileField('Update Profile 2', validators=[FileAllowed(['jpg', 'png'])])
    picture3 = FileField('Update Profile 2', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This registration no. is already registered.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already registered.')
