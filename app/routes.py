from app import app, db
from flask import Flask, render_template, redirect, request
from app.models import User, Post

@app.route('/')
def index():
    posts = db.session.query(Post).all()
    return render_template('index.html', posts=posts)