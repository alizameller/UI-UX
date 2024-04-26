from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import pyotp
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, text, Integer, String, Column, DateTime, ForeignKey, PrimaryKeyConstraint, func, select
from sqlalchemy.orm import sessionmaker, declarative_base, backref, relationship

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy()
# create the app
app = Flask(__name__)
app.secret_key = 'david_stekol'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/final_project"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True



# initialize the app with Flask-SQLAlchemy
db.init_app(app)

# Placeholder data for demonstration
tasks = [
    {"id": 1, "activity": "UI/UX", "name": "Homework", "details": "Details of Task 1", "start_time": "2024-04-08T15:40", "end_time": "2024-04-08T17:00", "priority": "High"},
    {"id": 2, "activity": "Databases", "name": "Presentation", "details": "Details of Task 2", "start_time": "2024-04-09T12:40", "end_time": "2024-04-09T15:00", "priority": "Medium"},
    {"id": 3, "activity": "Senior Projects", "name": "Meeting", "details": "Details of Task 2", "start_time": "2024-04-09T12:40", "end_time": "2024-04-09T15:00", "priority": "Medium"},
    {"id": 4, "activity": "Databases", "name": "Assignment", "details": "Details of Task 2", "start_time": "2024-04-10T12:40", "end_time": "2024-04-10T15:00", "priority": "Medium"},
]

colors = {"Databases": "rgb(226, 0, 246)", "UI/UX": "rgb(73, 246, 250)", "Senior Projects": "gray"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        masterkey = data.get('password')
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        db = engine.connect()
        cursor = db.execute(text(f'SELECT password FROM users WHERE username = \'{username}\''))
        password = cursor.fetchall()
        if not password:
            
            return jsonify({'message': 'User not found'}), 401

        if not check_password_hash(password[0][0], masterkey):
            return jsonify({'message': 'Incorrect password'}), 401

        session['username'] = username
        session['authenticated'] = False
        db.close()
        #return jsonify({'message': 'Login successful'})
        # Handle login logic here
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        db = engine.connect()
        cursor = db.execute(text(f'SELECT email FROM users WHERE email = \'{email}\''))
        user = cursor.fetchall()

        if user:
            return jsonify({'message': 'Email already has an associated account'}), 400

        db.execute(text(f'INSERT INTO users (email, password) VALUES (\'{email}\',\'{generate_password_hash(password)}\')'))
        db.commit()
        db.close()

        #return jsonify({'message': 'Registration successful'})
        # Handle signup logic here
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', tasks=tasks, colors=colors)

@app.route('/monthly_calendar')
def monthly_calendar():
    # Render your monthly_calendar.html template
    return render_template('monthly_calendar.html', tasks=tasks, colors=colors)

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/test_db')
def test_db():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

if __name__ == '__main__':
    app.run(debug=True)
