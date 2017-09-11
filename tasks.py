import os
from mods._celery import create_celery
from mods import app
from flask_mail import Message
from werkzeug.utils import secure_filename
from mods.extensions import mail, db
from mods.admin.models import File
from mods.admin.functions import _init_s3, _parse_contract_date


s3 = _init_s3()
celery = create_celery(app)


@celery.task
def send_mail(subject, recipients, html):
    msg = Message(subject,
                  recipients=[recipients],
                  html=html,
                  sender=app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)


@celery.task
def upload_to_s3(filename, file_content):
    s3.put_object(Bucket=os.environ.get('S3_BUCKET_NAME'), Key=filename, Body=file_content)
    url = '{}/{}/{}'.format(s3.meta.endpoint_url,
                            os.environ.get('S3_BUCKET_NAME'),
                            filename)
    symbol, contract_date = _parse_contract_date(filename)
    db.session.add(File(filename=filename,
                        path=url,
                        symbol=symbol,
                        contract_date=contract_date))


@celery.task
def download_from_s3(q):
    return s3.get_object(Bucket=os.environ.get('S3_BUCKET_NAME'),
                         Range='bytes={}-{}'.format(67, ''),
                         Key=q)['Body'].read().lstrip()


# def write_filetable(files):
    # for f in files:
        # filename = secure_filename(f.filename)[2:]
        # symbol, short_name, contract_date = _parse_contract_date(filename)
        # url = 'https://s3.amazonaws.com/{}/downloads2/{}/{}'.format(
               # os.environ.get('S3_BUCKET_NAME'), symbol, short_name)
        # db.session.add(File(filename=filename,
                        # path=url,
                        # symbol=symbol,
                        # contract_date=contract_date))
    # db.session.commit()
@celery.task
def write_filetable(filename, url, symbol, contract_date):
    db.session.add(File(filename=filename,
                   path=url,
                   symbol=symbol,
                   contract_date=contract_date))
    db.session.commit()

