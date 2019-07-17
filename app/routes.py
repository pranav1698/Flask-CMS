from app import app, db
from flask import Flask, render_template, redirect, request
from app.models import User, Post
from app.forms import LoginForm

def convertToBinaryData(filename):
#Convert digital data to binary format
	with open(filename, 'rb') as file:
		binaryData = file.read()
	return binaryData    

@app.route('/')
def index():
    posts = db.session.query(Post).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def view_post(post_id):
	post = db.session.query(Post).filter_by(id=post_id).first()
	date = str(post.timestamp)[:10]
	return render_template('post.html', title=post.title, body=post.body, date=date, username=post.username)

@app.route('/new_post')
def new_post():
	return render_template('new_post.html')

@app.route('/add_post',  methods = ['POST'])
def add_post():
	title = request.form['title']
	image_file = request.form['image']
	image = convertToBinaryData(image_file)
	body = request.form['body']
	username = "pranav"
	post = Post(title=title, body=body, image= image, username=username)
	db.session.add(post)
	db.session.commit()
	posts = db.session.query(Post).all()
	return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		email = form.email.data
		username = form.username.data
		password = form.password.data
		remember_me = form.remember_me.data
		user = User(username=username, email=email, password_hash=password)
		db.session.add(user)
		db.session.commit()
		return render_template('new_post.html')
	return render_template('login.html', title='Sign In', form=form)