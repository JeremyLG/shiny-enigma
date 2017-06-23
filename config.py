SECRET_KEY = "super secret key"

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_NAME = 'local'
MONGO_URI = 'mongodb://'+MONGODB_HOST+':'+str(MONGODB_PORT)+'/'+MONGODB_NAME
# email server
DEBUG = True
MAIL_SERVER = 'smtp.office365.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USERNAME = "jeremy.legall@42consulting.fr"
MAIL_PASSWORD = "HelicE35"

ADMINS = ['jeremy.legall@42consulting.fr']
