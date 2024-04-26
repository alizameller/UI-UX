from flask import Flask, render_template, request, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import create_engine, text, Integer, String, Column, DateTime, ForeignKey, PrimaryKeyConstraint, func, select
from sqlalchemy.orm import sessionmaker, declarative_base, backref, relationship

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

# INSERT INTO tasks (task_id, userid, task_name, task_details, task_duration, deadline, start_time, end_time) VALUES (1, 1, 'Homework', 'Details of Task 1', NULL, NULL, '2024-04-08T15:40', '2024-04-08T17:00')
# INSERT INTO tasks (task_id, userid, task_name, task_details, task_duration, deadline, start_time, end_time) VALUES (1, 1, 'Homework', 'Details of Task 1', NULL, NULL, '2024-04-08T15:40', '2024-04-08T17:00')  

colors = {"Databases": "rgb(226, 0, 246)", "UI/UX": "rgb(73, 246, 250)", "Senior Projects": "gray"}

Base = declarative_base()
class Users(Base):
    __tablename__ = 'users'

    email = Column(String, primary_key = True)
    userid = Column(Integer)
    password = Column(String)

    def __repr__(self):
        return "<User(email={self.email}, id={self.userid}, password={self.password})>" 
        # return [{'email':'%s','id':'%s','password':'%s'}] % (self.email, self.userid, self.password)
    
class Tasks(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key = True)
    userid = Column(Integer)
    task_name = Column(String)
    task_details = Column(String)
    task_duration = Column(DateTime)
    deadline = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    activity_id = Column(Integer)

    def __repr__(self):
        return "Task {self.task_id}" 
        # return [{'email':'%s','id':'%s','password':'%s'}] % (self.email, self.userid, self.password)

class Activities(Base):
    __tablename__ = 'activities'

    activity_id = Column(Integer, primary_key = True)
    activity_name = Column(String)
    userid = Column(Integer)
    time = Column(DateTime)    

    def __repr__(self):
        return "Activity {self.activity_id}" 
        # return [{'email':'%s','id':'%s','password':'%s'}] % (self.email, self.userid, self.password)

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
    new_tasks = db.session.query(Tasks.task_id, Tasks.task_name, Tasks.task_details, Tasks.start_time, Tasks.end_time, Activities.activity_name).join(Activities, (Tasks.activity_id == Activities.activity_id)).all()
    print(new_tasks)
    return render_template('dashboard.html', tasks=new_tasks, colors=colors)

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
        users = db.session.query(Users.email, Users.userid, Users.password).all()
        return render_template('test_db.html', users=users)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

if __name__ == '__main__':
    app.run(debug=True)
