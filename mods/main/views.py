from datetime import datetime
from flask import flash, Blueprint, request, current_app, render_template, url_for, redirect
from flask_login import current_user
from ..admin.models import Symbol, Inquiry
from ..app import app
from .._celery import create_celery
from ..extensions import db


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    return render_template('main/index.html',
                           title='home',
                           current_user=current_user)


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    celery = create_celery(current_app)
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        content = request.form.get('content')
        record = Inquiry(firstname=firstname, lastname=lastname,
                         email=email, phone=phone, subject=subject,
                         content=content, recieved_on=datetime.utcnow())

        db.session.add(record)
        db.session.commit()
        client_mail_content = "Dear {}, we've recieved your inquiry regarding {}. We will contact you shortly.".format(lastname, subject)
        int_mail_content = "You are assign to help customer on {}.".format(subject)
        flash('Your message has been sent. We will be touch soon.', 'success')
        celery.send_task('tasks.send_mail', args=(subject, email, client_mail_content))
        celery.send_task('tasks.send_mail', args=(subject, app.config['MAIL_DEFAULT_SENDER'], int_mail_content))
        return redirect(url_for('main.home'))
    return render_template('main/contact.html', current_user=current_user)


@main_bp.route('/about')
def about():
    return render_template('main/about.html', current_user=current_user)


@main_bp.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if query:
        return redirect(url_for(
            'main.search_result',
            query=query))
    return redirect(url_for('main.home'))


@main_bp.route('/search_result')
def search_result():
    query = request.args.get('query')
    results = Symbol.query.search(query).all()
    if results:
        flash('Here are the docs that we found.', 'success')
    else:
        flash('Nothing found. Please try other words.', 'danger')
    return render_template('main/results.html', query=query,
                           current_user=current_user,
                           title='results', results=results)


@main_bp.route('/filter_results')
def filter_results():
    query = request.args.get('query')
    symbol = request.args.get('symbol')
    name = request.args.get('name')
    exchange = request.args.get('exchange')
    category = request.args.get('category')
    Query = Symbol.query.search(query)
    if symbol:
        Query = Query.filter(Symbol.symbol==symbol)
    if name:
        Query = Query.filter(Symbol.name==name)
    if exchange:
        Query = Query.filter(Symbol.exchange==exchange)
    if category:
        Query = Query.filter(Symbol.category==category)
    results = Query.all()
    return render_template('main/results.html',
                           query=query,
                           current_user=current_user,
                           title='results', results=results)
