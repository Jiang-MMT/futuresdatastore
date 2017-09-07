from mods._celery import create_celery
from mods import app


celery = create_celery(app)
