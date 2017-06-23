from flask import render_template, flash, redirect, session, url_for, request, \
    g, jsonify
import datetime
from app import app, mongo
from .emails import send_email
from config import ADMINS
from werkzeug import check_password_hash, generate_password_hash
from bson.objectid import ObjectId

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
        print(session['user_id'] + "    " + str(g.user))

@app.route("/")
def index():
    return render_template("layout.html")

# @app.route('/author', methods=['GET'])
# def author():
#     error = None
#     author = mongo.db.author
#     output = []
#     for s in author.find():
#         output.append({'author' : s['author'], 'title' : s['title']})
#     return render_template('account.html',error=error)
    #return jsonify({'result' : output})

# @app.route('/user/<nickname>')
# @app.route('/user/<nickname>/<int:page>')
# def user(nickname, page=1):
#     user = User.query.filter_by(nickname=nickname).first()
#     if user is None:
#         flash(gettext('User %(nickname)s not found.', nickname=nickname))
#         return redirect(url_for('index'))
#     posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
#     return render_template('user.html',
#                            user=user,
#                            posts=posts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    mongo.db.messages.insert({"email":str(request.form['emaill']),"message":str(request.form['message'])})
    flash('You sent a message','success')
    send_email("Vous avez reçu un message",
                   ADMINS[0],
                   [ADMINS[0]],
                   render_template("email.txt",email=request.form['emaill'], message=request.form['message']),
                   render_template("email.html",email=request.form['emaill'], message=request.form['message']))
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
            mongo.db.users.insert({"username":request.form['username'],"email":request.form['email'],"avatar":"static/img/avatar.png","password":generate_password_hash(request.form['password']),"date":datetime.datetime.utcnow()})
            flash('You were successfully registered and can login now',"success")
            return redirect(url_for('index'))
    return render_template('register.html', error=error)

@app.route('/account', methods=['GET', 'POST'])
def account():
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
        elif ((g.user['username'] != request.form['username'])&(mongo.db.users.find_one(request.form['username']) is not None)):
            error = 'The username is already taken'
        else:
            mongo.db.users.update({'_id': ObjectId(session['user_id'])},{'_id': ObjectId(session['user_id']),'username':request.form['username'],'email':request.form['email'],'avatar':"static/img/avatar.png",'password':generate_password_hash(request.form['password']),"date":datetime.datetime.utcnow()})
            flash('You successfully edited your infos',"success")
            return redirect(url_for('index'))
    return render_template('account.html', error=error)

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
