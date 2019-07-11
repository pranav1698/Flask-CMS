from app import app, db
from flask import Flask, render_template, redirect, request
from app.models import User, Post

@app.route('/')
def index():
    posts = db.session.query(Post).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def view_post(post_id):
	post = db.session.query(Post).filter_by(id=post_id).first()
	date = str(post.timestamp)[:10]
	return render_template('post.html', title=post.title, body=post.body, date=date, username=post.username)