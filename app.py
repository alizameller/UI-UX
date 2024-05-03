from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pyotp
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, text, Integer, String, Column, DateTime, ForeignKey, PrimaryKeyConstraint, func, select
from sqlalchemy.orm import sessionmaker, declarative_base, backref, relationship
from datetime import datetime, timedelta

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy()
# create the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://alizameller:@localhost:5432/final_project"
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

# INSERT INTO tasks (task_id, userid, task_name, task_details, task_duration, deadline, start_time, end_time) VALUES (1, 1, 'Homework', 'Details of Task 1', NULL, NULL, '2024-04-08T15:40', '2024-04-08T17:00')
# INSERT INTO tasks (task_id, userid, task_name, task_details, task_duration, deadline, start_time, end_time) VALUES (1, 1, 'Homework', 'Details of Task 1', NULL, NULL, '2024-04-08T15:40', '2024-04-08T17:00')  

colors = {"Databases": "rgb(226, 0, 246)", "UI/UX": "rgb(73, 246, 250)", "Senior Projects": "gray"}

Base = declarative_base()
class Users(Base):
    __tablename__ = 'users'

    email = Column(String, primary_key = True)
    userid = Column(Integer, autoincrement=True)
    password = Column(String)

    def __repr__(self):
        return "<User(email={self.email}, id={self.userid}, password={self.password})>" 
        # return [{'email':'%s','id':'%s','password':'%s'}] % (self.email, self.userid, self.password)
    
class Tasks(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key = True, autoincrement=True)
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
        data = request.get_json()
        print(data)
        email = data.get('email')
        masterkey = data.get('password')
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        db = engine.connect()
        cursor = db.execute(text(f'SELECT password FROM users WHERE email = \'{email}\''))
        password = cursor.fetchall()
        if not password:
            return jsonify({'message': 'User not found'}), 401
        elif not check_password_hash(password[0][0], masterkey):
            return jsonify({'message': 'Incorrect password'}), 401
        else: 
            session['username'] = email
            print(session['username'])
            db.close()
            return jsonify({'message': 'User not found'}), 200
        # return render_template('dashboard.html', tasks=tasks, colors=colors)
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
    new_tasks = db.session.query(Tasks.task_id, Tasks.task_name, Tasks.task_details, Tasks.start_time, Tasks.end_time, Activities.activity_name).join(Activities, (Tasks.activity_id == Activities.activity_id)).order_by(func.age(Tasks.start_time).desc()).all()
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

@app.route('/events')
def events():
    return render_template('loading.html')

#Hardcoded data for now.
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        print((request.form['task_name']))
        print((request.form['details']))
        print((request.form['activity']))
        # print((request.form['duration_hrs']))
        # print((request.form['duration_mins']))
        print((request.form['deadline']))
        
        user_id = 1
        # task_id = 3
        task_name = request.form['task_name']
        task_details = request.form['details']
        # activity_id = 2
        task_duration = int(request.form['duration_hrs']) * 3600 + int((request.form['duration_mins'])) * 60
        print(task_duration)
        deadline = request.form['deadline']
        end_time = request.form['deadline']
        format_data = '%Y-%m-%dT%H:%M'
        id = db.session.query(Activities.activity_id).where(Activities.activity_name == request.form['activity']).all()
        if id[0][0]:
            activity_id = id[0][0]
            print(activity_id)

        try:
            new_task = Tasks(
                userid=user_id, 
                activity_id = activity_id,
                task_name=task_name,
                task_details=task_details,
                task_duration=timedelta(seconds=task_duration),
                deadline=datetime.strptime(deadline, format_data), 
                # start_time = datetime.strptime(start_time, format_data),
                end_time = datetime.strptime(end_time, format_data)
            )
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully!')
            # message = "Task added successfully!"
            #return render_template('add_task.html')
        except Exception as e:
            db.session.rollback()
            if (type(e).__name__) == "IntegrityError":
                message = "An internal error occured. \nPlease try again."
            if (type(e).__name__) == "ValueError":
                message = "An invalid datetime value was entered. \nPlease select a date from the dropdown calendar."
            # message = "An error occurred: {}".format(str(e))
            flash(message)
            #return render_template('add_task.html')
    return render_template('add_task.html')

#Hardcoded data for now.
@app.route('/add_activity', methods=['GET', 'POST'])
def add_activity():
    if request.method == 'POST':
        user_id = 1  
        activity_name = "Team Meeting"
        time = "2024-05-10"  
        activity_id = 2

        try:
            new_activity = Activities(
                userid=user_id,
                activity_id = activity_id,
                activity_name=activity_name,
                time=datetime.strptime(time, '%Y-%m-%d').date()  
            )
            db.session.add(new_activity)
            db.session.commit()
            return "Activity added successfully\n", 200
        except Exception as e:
            db.session.rollback()
            return "An error occurred: {0}".format(str(e)), 500
    return render_template('add_activity.html')
if __name__ == '__main__':
    app.run(debug=True)