import os

DB_NAME = '1l1s'
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = 'postgres'
DB_ENGINE = 'postgresql'

DB_URL = f'{DB_ENGINE}://{DB_USER}@{DB_HOST}/{DB_NAME}'
