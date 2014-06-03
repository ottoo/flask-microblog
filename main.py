from flask import Flask, request, g, url_for, render_template, redirect
from database import db_session
from models import User, Post

app = Flask(__name__)

# Removes db sessions at the end of request or when app shuts down
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Main route
@app.route('/')
def hello_world():
    return 'Hello World!'

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
@app.route('/posts/<postid>', methods=['GET'])
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

if __name__ == '__main__':
    app.run()
