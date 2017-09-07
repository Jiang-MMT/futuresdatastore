from functools import wraps
from flask import flash
from flask_login import current_user
from mods.extensions import login_manager


def role_required(roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('You are not authorized to view this page!', 'danger')
                return login_manager.unauthorized()
            if current_user.role not in roles:
                flash('You are not authorized to view this page!', 'danger')
                return login_manager.unauthorized()
            return f(*args, **kwargs)
        return wrapped
    return wrapper
