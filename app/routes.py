import os 
from app import app, db
from flask import Flask, render_template, redirect, request, url_for, send_from_directory, session
from flask_login import current_user, login_user
from app.models import User, Post
from werkzeug import secure_filename
from app.forms import RegisterForm, LoginForm
from base64 import b64encode

ALLOWED_EXTENSIONS_IMAGE = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = '/home/pranav/Desktop/Projects/Content/app/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_images(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE

def convertToBinaryData(filename):
#Convert digital data to binary format
	with open(filename, 'rb') as file:
		binaryData = file.read()
	return binaryData    

#Root route to the server
@app.route('/')
def index():
    posts = db.session.query(Post).all()
    added_posts = list()
    for post in posts:
    	post_1 = {}
    	post_1['id'] = post.id
    	post_1['title'] = post.title
    	post_1['body'] = post.body
    	post_1['username'] = post.username
    	post_1['date'] = str(post.timestamp)[:10]
    	if post.image:
    		post_1['image'] = b64encode(post.image).decode("utf-8")
    	added_posts.append(post_1)
    return render_template('index.html', posts=added_posts)

#API to fetch a specifies post from server
@app.route('/post/<int:post_id>')
def view_post(post_id):
	post = db.session.query(Post).filter_by(id=post_id).first()
	image = None
	if post.image:
		image = b64encode(post.image).decode("utf-8")
	date = str(post.timestamp)[:10]
	return render_template('post.html', title=post.title, body=post.body, date=date, username=post.username, image=image)

#Open new post page
@app.route('/new_post')
def new_post():
	if 'username' in session:
		username = session['username']
		return render_template('new_post.html', username=username)
	return render_template('new_post.html', username="")

#API to create a new post request to the server
@app.route('/add_post',  methods = ['POST'])
def add_post():
	db.session.rollback()
	title = request.form['title']
	image_file = request.files['image']
	if image_file:
		if allowed_images(image_file.filename):
			filename = secure_filename(image_file.filename)
			image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			filename = app.config['UPLOAD_FOLDER'] + filename
	image = convertToBinaryData(filename)
	body = request.form['body']
	username = session["username"]
	post = Post(title=title, body=body, image= image, username=username)
	db.session.add(post)
	db.session.commit()
	return redirect(url_for('index'))

#API to create a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		email = form.email.data
		username = form.username.data
		password = form.password.data
		remember_me = form.remember_me.data
		user = User(username=username, email=email)
		user.set_password(password)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

#API to login a already registered user
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('new_post'))
	form = LoginForm()
	if form.validate_on_submit():
		username=form.username.data
		user = User.query.filter_by(username=username).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		session['username'] = username
		return redirect(url_for('new_post'))
	return render_template('login.html', form=form)

