from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://localhost:27017/')

mydb = client.local

mydb.collection_names()

mydb.create_collection('author')
myrecord = {"author": "Duke",  "title" : "PyMongo 101",  "tags" : ["MongoDB", "PyMongo", "Tutorial"],  "date" : datetime.datetime.utcnow()  }
mydb.author.insert_one(myrecord)

myco = mydb.test

import datetime

from werkzeug import generate_password_hash
passtest = generate_password_hash("new")
passtest
mydb.drop_collection('messages')
mydb.create_collection('messages')
mydb.drop_collection('users')
mydb.create_collection('users')
myrecord = {"username":"admin","email":"email.test@newx.fr","password":passtest,"date" : datetime.datetime.utcnow()  }
myrecord
mydb.users.insert_one(myrecord)
for s in mydb.messages.find():
    print(s)
tt = mydb.test.find_one({"author":"Duke"})
tt == None
tt is None
tt
tt['title']
check_password_hash('new','nw')
