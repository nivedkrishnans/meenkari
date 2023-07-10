# IMPORTANT: During deployment set up a random SECRET_KEY_DEPLOY environment variable
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = os.environ.get('DATABASE_URL')

#if the SECRET_KEY_DEPLOY environment variabe is available use that else use this random string
SECRET_KEY_DEPLOY = os.environ.get('SECRET_KEY_DEPLOY')
SECRET_KEY = SECRET_KEY_DEPLOY if SECRET_KEY_DEPLOY else ";+h!7qsT<;n%<yTI/~N9c\g?cpBH{tJ9ui,V5mVzkMf-W?BlxQnvO"

#change DEBUG to False for production
DEBUG = True

#add your respective hostname(s) to the ALLOWED_HOSTS list
ALLOWED_HOSTS = ["*"]

#if the DATABSE_URL variable is found like in heroku, it uses that, otherwise uses the database provided in DB_temp
import dj_database_url
DB_temp = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True) if DATABASE_URL else DB_temp


#for gmail, use the following
#EMAIL_BACKEND = ‘django.core.mail.backends.smtp.EmailBackend’
#EMAIL_HOST = ‘smtp.gmail.com’
#EMAIL_USE_TLS = True
#EMAIL_PORT = 587
#EMAIL_HOST_USER = ‘your_account@gmail.com’
#EMAIL_HOST_PASSWORD = ‘your account’s password’
