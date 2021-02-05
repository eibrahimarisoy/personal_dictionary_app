from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        [DataRequired("Username field cannot be empty")]
    )
    password = PasswordField(
        'Password',
        [DataRequired("Password field cannot be empty")]
    )
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        [DataRequired("Username field cannot be empty")]
    )
    password = PasswordField(
        'Password',
        [DataRequired("Password field cannot be empty")]
    )
    submit = SubmitField('Login')


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        [DataRequired("ExPassword field cannot be empty")]
    )
    new_password = PasswordField(
        'New Password',
        [DataRequired("Password field cannot be empty")]
    )
    submit = SubmitField('Change')
