from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from app.models import USER
from werkzeug.security import generate_password_hash, check_password_hash


class signUpForm(FlaskForm):
    user_name = StringField('User name ', validators=[DataRequired(), Length(min=5, message=('Your id is too short'))])
    full_name = StringField('Full Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message=('Your password is too short'))])
    rePassword = PasswordField('reType Password', validators=[DataRequired(), EqualTo('password', message=('Password must match'))])
    email = StringField('Email', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[("Nam", "Nam"), ("Nữ", "Nữ"), ("Khác", "Khác")])
    phone = IntegerField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Sign up')

    def validate_user_name(self, user_name):
        user_name = USER.query.filter_by(user_name=user_name.data).first()
        if user_name is not None:
            raise ValidationError('Username has been already used! Please use a different username')

    def validate_email(self, email):
        email = USER.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Email has been already used! Please use a different email ')


class loginForm(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('sign in')


class addSHOPForm(FlaskForm):
    name = StringField('Name')
    address = StringField('Address')
    img = StringField('Image')
    level = IntegerField('Level')
    lat = StringField('Lat')
    lng = StringField('Lng')
    submit = SubmitField('Add')
