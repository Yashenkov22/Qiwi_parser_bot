import os
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.environ.get('TOKEN_API')

# DATABASE
DB_USER = os.environ.get('DB_USER')
DB_NAME = os.environ.get('DB_NAME')
DB_PASS = os.environ.get('DB_PASS')


#QIWI SIGN IN
QIWI_LOGIN = os.environ.get('QIWI_LOGIN')
QIWI_PASS = os.environ.get('QIWI_PASS')


db_url = URL.create(
    'mysql',
    username=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    host='localhost',
    port=6033,
)