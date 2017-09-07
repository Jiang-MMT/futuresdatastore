from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def gen_confirmation_token(email):
    ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return ts.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=7200):
    ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = ts.loads(token,
                         salt=current_app.config['SECURITY_PASSWORD_SALT'],
                         max_age=expiration)
    except:
        return False
    return email
