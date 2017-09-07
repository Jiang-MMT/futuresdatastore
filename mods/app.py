from flask import Flask, render_template, flash, url_for, redirect, request
from sqlalchemy_searchable import make_searchable
from user import User
from extensions import db, mail, login_manager, bcrypt


def configure_extensions(app):
    db.init_app(app)
    # login_manager.refresh_view = 'user.reauth'
    login_manager.init_app(app)
    @login_manager.user_loader
    def user_loader(user_email):
        return User.query.filter_by(email=user_email).first()
    login_manager.login_view = 'user.signin'
    login_manager.login_message_category = "info"
    mail.init_app(app)
    bcrypt.init_app(app)


def configure_blueprints(app):
    from user import user_bp
    from main import main_bp
    from resource import resource_bp
    for bp in [user_bp, main_bp, resource_bp]:
        app.register_blueprint(bp)


def configure_hook(app):
    @app.before_request
    def before_request():
        pass


def configure_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error.html', message='403 forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', message='404 not found'), 404

    @app.errorhandler(410)
    def gone(e):
        return render_template('error.html', message='410 gone'), 410

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('error.html', message='500 internal error'), 500


def configure_cli(app):
    @app.cli.command()
    def initdb():
        db.drop_all()
        make_searchable()
        db.configure_mappers()
        db.create_all()


app = Flask(__name__)
app.config.from_object('config')
configure_blueprints(app)
configure_extensions(app)
configure_error_handlers(app)
configure_cli(app)

from admin import views
