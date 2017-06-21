from flask import Flask, request, session, url_for, redirect,jsonify,render_template, abort, g, flash, _app_ctx_stack
from flask_pymongo import PyMongo
from werkzeug import check_password_hash, generate_password_hash
import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_NAME = 'local'

app.config['MONGO_DBNAME'] = 'mydb'
app.config['MONGO_URI'] = 'mongodb://'+MONGODB_HOST+':'+str(MONGODB_PORT)+'/'+MONGODB_NAME
app.secret_key = "super secret key"
mongo = PyMongo(app)

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = mongo.db.test.find_one({'_id': ObjectId(session['user_id'])})
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
    if request.method == 'POST':
        return "Vous avez envoyé un message..."
    return '<form action="" method="post"><input type="text" name="msg" /><input type="submit" value="Envoyer" /></form>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        user = mongo.db.test.find_one({"username":request.form['username']})
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['password'],request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
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
        elif mongo.db.test.find_one(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            mongo.db.test.insert({"username":request.form['username'],"email":request.form['email'],"password":generate_password_hash(request.form['password']),"date":datetime.datetime.utcnow()})
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
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
