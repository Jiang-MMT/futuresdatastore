import os


DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY')
SECURITY_PASSWORD_SALT = 'confirmation email'
# Bcyrpt
BCRYPT_LOG_ROUNDS = 12
# Wtform
WTF_CSRF_ENABLED = True
# Database
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
# Mail
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
# Celery
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
ACCEPT_CONTENT = ['json']
CELERY_IMPORTS = ('tasks')
# S3
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
SYMBOL_BUCKET = os.environ.get('SYMBOL_BUCKET')
