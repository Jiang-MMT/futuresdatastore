from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, validators


class signupForm(FlaskForm):
    email = TextField('email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('password', [validators.DataRequired()])


class signinForm(FlaskForm):
    email = TextField('email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('password', [validators.DataRequired()])


class resendForm(FlaskForm):
    email = TextField('email', [validators.DataRequired(), validators.Email()])


class forgotForm(FlaskForm):
    email = TextField('email', [validators.DataRequired(), validators.Email()])


class resetForm(FlaskForm):
    password = PasswordField('password', [validators.DataRequired()])


class changepwdForm(FlaskForm):
    old_pwd = PasswordField('password', [validators.DataRequired()])
    new_pwd = PasswordField('password', [validators.DataRequired()])
