import os
import contextlib
from StringIO import StringIO
from datetime import datetime
from flask import(Blueprint, render_template, request,
                  url_for, current_app, Response, flash, redirect)
from flask_login import current_user, login_required
# from mods.app import app
from ..admin.models import File
from forms import DownloadForm
from ..admin.functions import _init_s3
# from .._celery import create_celery


resource_bp = Blueprint('resource', __name__, url_prefix='/resource')


@resource_bp.route('/download_query', methods=['GET', 'POST'])
@login_required
def download_query():
    form = DownloadForm()
    symbol = request.args.get('symbol')
    if request.method == 'POST':
        if symbol:
            form.symbol.data = symbol
        symbol = form.symbol.data.upper()
        start = form.contract_from.data
        end = form.contract_to.data
        results = File.query.filter(File.symbol == symbol,
                                    File.contract_date.between(start, end)).all()
        if results:
            return redirect(url_for('resource.show_results',
                                    symbol=symbol, start=start, end=end))
        else:
            flash('The file does not exist.', 'danger')
            return redirect(request.url)
    return render_template('resource/download_query.html',
                           title='Download_query',
                           form=form,
                           current_user=current_user)


@resource_bp.route('/show_results', methods=['GET', 'POST'])
@login_required
def show_results():
    symbol = request.args.get('symbol')
    start = request.args.get('start')
    end = request.args.get('end')
    results = File.query.filter(File.symbol == symbol,
                                File.contract_date.between(start, end)).all()
    if request.method == 'POST':
        query = request.form.getlist('csv')
        return redirect(url_for('resource.download_csv', query=query))
    return render_template('resource/show_results.html',
                           current_user=current_user,
                           results=results,
                           title='show results')


@resource_bp.route('/download_csv')
@login_required
def download_csv():
    s3 = _init_s3()
    # celery = create_celery(current_app)
    query = request.args.getlist('query')
    if query:
        with contextlib.closing(StringIO()) as b:
            b.write('symbol,timestamp,tradingDay,open,high,low,close,volume,openInterest\n')
            for q in query:
                directory = q[:1]
                obj_name = q
                # directory = q.split('_')[0]
                # obj_name = q.split('_')[-1]
                k = 'downloads2/{}/{}'.format(directory, obj_name)
                data = s3.get_object(Bucket=os.environ.get('S3_BUCKET_NAME'),
                                     Range='bytes={}-{}'.format(67, ''),
                                     Key=k)['Body'].read().lstrip()
                b.write(data)
            return Response(b.getvalue(),
                            mimetype='text/csv',
                            headers={"Content-Disposition": "attachment;filename={}.csv".format(datetime.utcnow())})
    else:
        flash('Please select file(s)', 'danger')
        return redirect(url_for('resource.show_results'))
