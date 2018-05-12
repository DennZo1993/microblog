from flask import render_template

from app import app


@app.route('/')
@app.route('/index')
def index():
  user = {'username': 'Denis'}
  posts = [
    {
      'author': user,
      'body': 'My first post',
    },
  ]
  return render_template('index.html', title='Home', user=user, posts=posts)
