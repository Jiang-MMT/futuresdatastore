from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from ..extensions import db, bcrypt
from user_constants import USER_ROLE


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    _password = db.Column(db.String(128))
    role = db.Column(db.String, default=USER_ROLE['USER'])
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, plaintext):
        self.email = email
        self.password = plaintext

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def get_id(self):
        return self.email

    def get_role(self):
        return self.role
