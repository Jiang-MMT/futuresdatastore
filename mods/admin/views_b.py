from flask import request, redirect, url_for, flash
from flask_login import current_user
from flask_admin import Admin, BaseView, expose, AdminIndexView
from mods.app import app
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import secure_filename
from mods.extensions import db
from functions import _parse_contract_date, _load_csv_to_db, _init_s3
from ..user.models import User
from models import Symbol, File
from .._celery import create_celery


s3 = _init_s3()


class FileUploadView(BaseView):
    def is_accessible(self):
        if current_user.is_anonymous:
            return False
        if current_user.role not in ('admin',):
            return False
        return True

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                flash('You are not authorized to view this page.', 'danger')
                return redirect(url_for('main.home'))

    @expose('/', methods=('GET', 'POST'))
    def upload(self):
        if request.method == 'POST':
            if 'folder' in request.files:
                files = request.files.getlist('folder')
                for f in files:
                    filename = secure_filename(f.filename)
                    s3.upload_fileobj(f, app.config['UPLOAD_BUCKET'],
                                      filename)
                    url = '{}/{}/{}'.format(s3.meta.endpoint_url,
                                            app.config['UPLOAD_BUCKET'],
                                            filename)
                    symbol, contract_date = _parse_contract_date(filename)
                    db.session.add(File(filename=filename,
                                        path=url,
                                        symbol=symbol,
                                        contract_date=contract_date))
                db.session.commit()
                flash("Your files have been successfully uploaded!", "success")
                return redirect(request.url)
            return redirect(request.url)
        return self.render('admin/upload_file.html')

    @expose('/upload_csv', methods=('GET', 'POST'))
    def upload_csv(self):
        if request.method == 'POST':
            # try:
            if 'files' in request.files:
                files = request.files.getlist('files')
                for f in files:
                    _load_csv_to_db(f=f, db=db, model=Symbol)
                flash('Your files have been successfully uploaded!', 'success')
                return redirect(url_for('symbol.index_view'))
        return self.render('admin/upload_csv.html')


class MyHomeView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_anonymous:
            return False
        if current_user.role not in ('admin',):
            return False
        return True

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                flash('You are not authorized to view this page.', 'danger')
                return redirect(url_for('main.home'))
            else:
                return redirect(url_for('user.signin', next=request.url))


class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_anonymous:
            return False
        if current_user.role not in ('admin',):
            return False
        return True

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                flash('You are not authorized to view this page.', 'danger')
                return redirect(url_for('main.home'))
            else:
                return redirect(url_for('user.signin', next=request.url))


admin = Admin(app, index_view=MyHomeView(name='Dashboard'),
              base_template='admin_layout.html',
              template_mode='bootstrap3')
admin.add_view(MyModelView(User, db.session, endpoint='manage_user'))
admin.add_view(MyModelView(Symbol, db.session, endpoint='symbol'))
admin.add_view(FileUploadView(name='Files', endpoint='files'))
