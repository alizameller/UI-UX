from flask import Flask, render_template, request, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import create_engine, text, Integer, String, Column, DateTime, ForeignKey, PrimaryKeyConstraint, func, select
from sqlalchemy.orm import sessionmaker, declarative_base, backref, relationship
from datetime import datetime, timedelta

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy()
# create the app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://alizameller:@localhost:5432/final_project"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

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

# Task Model
class Task(db.Model):
    __tablename__ = 'tasks'
    Task_id = db.Column(db.Integer, primary_key=True)
    Userid = db.Column(db.Integer, nullable=False)
    Task_name = db.Column(db.String(100), nullable=False)
    Task_details = db.Column(db.String(500))
    Task_duration = db.Column(db.Interval)
    Deadline = db.Column(db.Date)

# Activity model
class Activity(db.Model):
    __tablename__ = 'activities'
    activity_id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(100), nullable=False)
    Userid = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup logic here
        return redirect(url_for('dashboard'))
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

#Hardcoded data for now. can replace with passed in data
@app.route('/add_task', methods=['POST'])
def add_task():
    user_id = 1
    task_name = "Develop Flask App"
    task_details = "Create a RESTful service with Flask"
    task_duration = 3600  
    deadline = "2024-05-10"

    try:
        new_task = Task(
            Userid=user_id,
            Task_name=task_name,
            Task_details=task_details,
            Task_duration=datetime.timedelta(seconds=task_duration),
            Deadline=datetime.datetime.strptime(deadline, '%Y-%m-%d').date()
        )
        db.session.add(new_task)
        db.session.commit()
        return "Task added successfully", 200
    
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}", 500

#Hardcoded data for now. can replace with passed in data
@app.route('/add_activity', methods=['POST'])
def add_activity():
    user_id = 1
    activity_name = "Team Meeting"
    time = "2024-05-10 14:00:00"

    try:
        new_activity = Activity(
            Userid=user_id,
            activity_name=activity_name,
            time=datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        )
        db.session.add(new_activity)
        db.session.commit()
        return "Activity added successfully", 200
    
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)