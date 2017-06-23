from flask import Flask, request, session, url_for, redirect,jsonify,render_template, abort, g, flash, _app_ctx_stack
from flask_pymongo import PyMongo
from werkzeug import check_password_hash, generate_password_hash
import datetime
from bson.objectid import ObjectId
import os


app = Flask(__name__)
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_NAME = 'local'

# email server
MAIL_SERVER = 'smtp.office365.com'
MAIL_PORT = 587
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USERNAME = "jeremy.legall@42consulting.fr"
MAIL_PASSWORD = "HelicE35"

ADMINS = ['jeremy.legall@42consulting.fr']
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.office365.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'jeremy.legall@42consulting.fr',
    MAIL_PASSWORD = 'HelicE35',))
from flask_mail import Mail
mail = Mail(app)
from flask_mail import Message
from app import app, mail
msg = Message('test subject', sender=ADMINS[0], recipients=[""])
msg.body = 'text body'
msg.html = '<b>HTML</b> body'
with app.app_context():
    mail.send(msg)

# administrator list
ADMINS = ['your-gmail-username@gmail.com']
app.config['MONGO_DBNAME'] = 'mydb'
app.config['MONGO_URI'] = 'mongodb://'+MONGODB_HOST+':'+str(MONGODB_PORT)+'/'+MONGODB_NAME
app.secret_key = "super secret key"
mongo = PyMongo(app)

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
        print(session['user_id'] + "    " + str(g.user))

@app.route("/")
def index():
    return render_template("layout.html")

@app.route('/author', methods=['GET'])
def author():
    error = None
    author = mongo.db.author
    output = []
    for s in author.find():
        output.append({'author' : s['author'], 'title' : s['title']})
    return render_template('account.html',error=error)
    #return jsonify({'result' : output})

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    mongo.db.messages.insert({"email":str(request.form['emaill']),"message":str(request.form['message'])})
    flash('You sent a message','success')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        user = mongo.db.users.find_one({"username":request.form['username']})
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['password'],request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in',"success")
            session['user_id'] = str(user['_id'])
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    # if g.user:
    #     return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif mongo.db.users.find_one(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            mongo.db.users.insert({"username":request.form['username'],"email":request.form['email'],"password":generate_password_hash(request.form['password']),"date":datetime.datetime.utcnow()})
            flash('You were successfully registered and can login now',"success")
            return redirect(url_for('index'))
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out',"info")
    session.pop('user_id', None)
    return redirect(url_for('index'))
# @app.route("/donorschoose/projects")
# def donorschoose_projects():
#     connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
#     collection = connection[DBS_NAME][COLLECTION_NAME]
#     projects = collection.find(projection=FIELDS, limit=100000)
#     #projects = collection.find(projection=FIELDS)
#     json_projects = []
#     for project in projects:
#         json_projects.append(project)
#     json_projects = json.dumps(json_projects, default=json_util.default)
#     connection.close()
#     return json_projects

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
