from flask import Flask, request, g, url_for, render_template, redirect, flash
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from database import db_session
from models import User, Post

app = Flask(__name__)
app.secret_key = 'jxb1Exxec1?74}A,xf0:xe9xb3xb3xfcxf1x87xf4xaaxc0'

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

# Removes db sessions at the end of request or when app shuts down
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Loads the front page and the posts from db
@app.route('/')
def mainpage():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('posts.html', posts=posts)

# Admin panel
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

# Searches topics
@app.route('/search')
def search():
    return render_template('search.html')

# Looks up a specific user from the db
@app.route('/profile/<username>')
def profile(username):
    username = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', username = username)

# Gets all users that contain a search string
@app.route('/users', methods=['GET', 'POST'])
def searchuser():
    if request.method == 'POST':
        search_string = request.form['text']
        usernames = User.query.filter(User.username.contains(search_string)).all()
        return render_template('userlist.html', usernames=usernames)

# Gets all posts
@app.route('/posts', methods=['GET'])
def getposts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)

# Gets a specific post
@app.route('/posts/<postid>')
def getpost(postid):
    post = Post.query.get(postid)
    return render_template('post.html', post=post)

# Inserts an user
@app.route('/user/insert')
def insertuser():
    user = User('guest1', 'guest1@test.com', 'guest1')
    db_session.add(user)
    db_session.commit()
    return render_template('search.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect(url_for('login'))
    if user.verify_password(password):
        login_user(user)
        flash("Logged in")
        return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
