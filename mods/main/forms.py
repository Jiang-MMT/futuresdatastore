from flask_wtf import FlaskForm
from wtforms import StringField, TextField, TextAreaField, validators


class ContactForm(FlaskForm):
    firstname = TextField('firstname', [validators.DataRequired()])
    lastname = TextField('lastname', [validators.DataRequired()])
    email = StringField('email', [validators.DataRequired(), validators.Email()])
    phone = StringField('phone', [validators.Optional()])
    subject = StringField('subject', [validators.DataRequired()])
    content = TextAreaField('content', [validators.DataRequired()])
