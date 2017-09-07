import os


BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
ACCEPT_CONTENT = ['json']
