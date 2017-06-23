import os

SECRET_KEY = "super secret key"

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_NAME = 'local'
MONGO_URI = 'mongodb://'+MONGODB_HOST+':'+str(MONGODB_PORT)+'/'+MONGODB_NAME
# email server
DEBUG = True
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

ADMINS = ['jeremy35.legall@gmail.com']
