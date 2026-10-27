import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for
from lib.post import Post
from lib.post_repository import PostRepository
from lib.database_connection import get_flask_database_connection

app = Flask(__name__)

@app.route('/')
def index():
    connection = get_flask_database_connection(app)
    post_repository = PostRepository(connection)
    posts = post_repository.all()
    return render_template('index.html', posts=posts)

# get posts for a given tag
@app.route('/tag/<tag>', methods=['GET', 'POST'])
def posts_by_tag(tag):
    connection = get_flask_database_connection(app)
    post_repository = PostRepository(connection)
    posts = post_repository.get_all_posts_by_tag(tag)
    return render_template('index.html', posts=posts)

# create new post
@app.route('/posts', methods=['POST'])
def create_post():
    connection = get_flask_database_connection(app)
    post_repository = PostRepository(connection)
    tags = [t.strip() for t in request.form['tags'].split(',') if t.strip()]
    new_post = Post(request.form['title'], request.form['content'], tags)
    post_repository.create(new_post)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)