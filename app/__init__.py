from flask import Flask
from flask_mail import Mail
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME,MAIL_PASSWORD,MONGODB_NAME,MONGO_URI
from flask_pymongo import PyMongo

print("MAIL USERNAME : " + MAIL_USERNAME)
app = Flask(__name__)
app.config.from_object('config')

mongo = PyMongo(app)

mail = Mail(app)

from app import views
