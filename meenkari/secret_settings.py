import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#create a random string for SECRET_KEY for your project
SECRET_KEY = ";+h!7qsT<;n%<yTI/~N9c\g?cpBH{tJ9ui,V5mVzkMf-W?BlxQnvO"

#change DEBUG to False for production
DEBUG = True

#add your respective hostname(s) to the ALLOWED_HOSTS list
ALLOWED_HOSTS = ['127.0.0.1']

#this is the defult sqlite databse. make appropriate changes
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


#for gmail, use the following
#EMAIL_BACKEND = ‘django.core.mail.backends.smtp.EmailBackend’
#EMAIL_HOST = ‘smtp.gmail.com’
#EMAIL_USE_TLS = True
#EMAIL_PORT = 587
#EMAIL_HOST_USER = ‘your_account@gmail.com’
#EMAIL_HOST_PASSWORD = ‘your account’s password’