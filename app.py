from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, send_from_directory
from pform import registrationForm, LoginForm
import os
from RAG import RAG
import asyncio
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pythonic.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config[
    "SECRET_KEY"
] = "62913a7dac3933f87a84626fcdeaaf9e2653f0a000843efd9bf2b31ba4767402"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_message_category="info"
# Define User model
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")


    def __repr__(self):
        return f"User('{self.fname}', '{self.lname}', '{self.username}', '{self.email}')"




with app.app_context():
    db.create_all()

###################################################################
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    return render_template('home.html')

###################################################################
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            image_file='default.jpg'
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for("login"))
    return render_template('register.html', form=form)

#####################################################################  
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been logged in!", "success")
            return redirect(url_for("chat"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template('login.html', form=form, title='Login')

@app.route('/chatbot', methods=['GET', 'POST'])
def chat():
    return render_template('chatbot.html')
###################################################################
@app.route("/logout" , methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for("home"))
###################################################################3
@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'}), 400 
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if file and file.filename.endswith('.pdf'):
        file.filename = 'input.pdf'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({'message': 'PDF uploaded successfully', 'filename': file.filename}), 200
    else:
        return jsonify({'error': 'File not uploaded'}), 400

#####################################################################
@app.route('/uploads/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#####################################################################
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    rag = RAG()
    app.logger.info("--------------------------------------------------------------")
    user_question = data['message']
    pdf_docs = "./uploads/input.pdf"
    if not user_question:
        return jsonify({'error': 'No message provided'}), 400
    answer = asyncio.run(rag.model(pdf_docs, user_question))
    app.logger.info("--------------------------------------------------------------")
    app.logger.info(answer)
    return jsonify({'response': answer}), 200

#####################################################################
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
