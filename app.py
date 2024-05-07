from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
import pyotp
from datetime import timedelta
import datetime
from sqlalchemy.sql import text, cast
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, text, Integer, String, Column, DateTime, ForeignKey, PrimaryKeyConstraint, func, select
from sqlalchemy.orm import sessionmaker, declarative_base, backref, relationship
from datetime import datetime, timedelta

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy()
# create the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'alizameller'
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://postgres:aliza@/final_project'
    '?host=/cloudsql/nth-bounty-422602-d8:us-central1:task-manager-db'
)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://alizameller:@localhost:5432/final_project"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SESSION_COOKIE_SECURE'] = True
# app.config['SESSION_COOKIE_HTTPONLY'] = True

# initialize the app with Flask-SQLAlchemy
db.init_app(app)
# Placeholder data for demonstration
# tasks = [
#     {"id": 1, "activity": "UI/UX", "name": "Homework", "details": "Details of Task 1", "start_time": "2024-04-08T15:40", "end_time": "2024-04-08T17:00", "priority": "High"},
#     {"id": 2, "activity": "Databases", "name": "Presentation", "details": "Details of Task 2", "start_time": "2024-04-09T12:40", "end_time": "2024-04-09T15:00", "priority": "Medium"},
#     {"id": 3, "activity": "Senior Projects", "name": "Meeting", "details": "Details of Task 2", "start_time": "2024-04-09T12:40", "end_time": "2024-04-09T15:00", "priority": "Medium"},
#     {"id": 4, "activity": "Databases", "name": "Assignment", "details": "Details of Task 2", "start_time": "2024-04-10T12:40", "end_time": "2024-04-10T15:00", "priority": "Medium"},
# ]

# INSERT INTO tasks (task_id, userid, task_name, task_details, task_duration, deadline, start_time, end_time) VALUES (1, 1, 'Homework', 'Details of Task 1', NULL, NULL, '2024-04-08T15:40', '2024-04-08T17:00')
# INSERT INTO tasks (task_id, userid, task_name, task_details, task_duration, deadline, start_time, end_time) VALUES (1, 1, 'Homework', 'Details of Task 1', NULL, NULL, '2024-04-08T15:40', '2024-04-08T17:00')  

# colors = {"Databases": "rgb(226, 0, 246)", "UI/UX": "rgb(73, 246, 250)", "Senior Projects": "gray"}

Base = declarative_base()
class Users(Base):
    __tablename__ = 'users'

    email = Column(String, primary_key = True)
    userid = Column(Integer, autoincrement=True, primary_key=True)
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
    userid = Column(Integer)
    activity_name = Column(String)
    activity_details = Column(String)
    start_time = Column(DateTime)    
    end_time = Column(DateTime)
    color = Column(String)

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
        email = data.get('email')
        masterkey = data.get('password')
        password = db.session.query(Users.password).where(Users.email == email).all()
        if not password:
            return jsonify({'message': 'User not found'}), 401
        elif not check_password_hash(password[0][0], masterkey):
            return jsonify({'message': 'Incorrect password'}), 401
        else: 
            session['username'] = email
            print(session['username'])
            return jsonify({'message': 'User found'}), 200
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = db.session.query(Users.email).where(Users.email == email).all()
        if user:
            return jsonify({'message': 'Email already has an associated account'}), 400
        new_user = Users(
                email=email,
                password = generate_password_hash(password),
                userid = None
            )
        db.session.add(new_user)
        session['username'] = email
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    print(session)
    if not session:
      return redirect('/')
    user_id = db.session.query(Users.userid).where(Users.email == session['username']).all()
    user_id = user_id[0][0]
    tasks = db.session.query(Tasks.task_id, Tasks.task_name, Tasks.task_details, Tasks.task_duration, Tasks.deadline, Tasks.start_time, Tasks.end_time, Activities.activity_name, Activities.color).join(Activities, (Tasks.activity_id == Activities.activity_id)).where(Tasks.userid == user_id).order_by(func.age(Tasks.end_time).desc()).all()
    #print(tasks)
    todays_datetime = (datetime.today()).date(),
    # print(todays_datetime)
    activities = db.session.query(Activities.activity_id, Activities.activity_name, Activities.activity_details, Activities.start_time, Activities.end_time).filter(func.date(Activities.start_time) == todays_datetime).where(Activities.userid == user_id).order_by(func.age(Activities.start_time).desc()).all()
    # print(new_activities)
    if request.method == 'POST':
        # prioritized = db.session.query(Tasks.task_id, Tasks.task_name, Tasks.task_details, Tasks.task_duration, Tasks.deadline, Tasks.start_time, Tasks.end_time, Activities.activity_name, Activities.color, ((datetime.now()-Tasks.end_time) + timedelta(microseconds=1)) - Tasks.task_duration).join(Activities, (Tasks.activity_id == Activities.activity_id)).order_by((((datetime.now()-Tasks.end_time) + timedelta(microseconds=1)) - Tasks.task_duration).asc()).all()
        # print(prioritized)
        return jsonify({'message': 'Success!'}), 200
    else:
        return render_template('dashboard.html', tasks=tasks, activities=activities)

@app.route('/new_dashboard', methods=['GET', 'POST'])
def new_dashboard():
    #print(tasks)
    if not session:
      return redirect('/')
    user_id = db.session.query(Users.userid).where(Users.email == session['username']).all()
    user_id = user_id[0][0]

    todays_datetime = (datetime.today()).date(),
    # print(todays_datetime)
    new_activities = db.session.query(Activities.activity_id, Activities.activity_name, Activities.activity_details, Activities.start_time, Activities.end_time).filter(func.date(Activities.start_time) == todays_datetime).where(Activities.userid == user_id).order_by(func.age(Activities.start_time).desc()).all()
    # print(new_activities)
    prioritized = db.session.query(Tasks.task_id, Tasks.task_name, Tasks.task_details, Tasks.task_duration, Tasks.deadline, Tasks.start_time, Tasks.end_time, Activities.activity_name, Activities.color, ((datetime.now()-Tasks.end_time) + timedelta(microseconds=1)) - Tasks.task_duration).join(Activities, (Tasks.activity_id == Activities.activity_id)).where(Tasks.userid == user_id).order_by((((datetime.now()-Tasks.end_time) + timedelta(microseconds=1)) - Tasks.task_duration).asc()).all()
    return render_template('new_dashboard.html', tasks=prioritized, activities=new_activities)

@app.route('/monthly_calendar')
def monthly_calendar():
    if not session:
      return redirect('/')
    user_id = db.session.query(Users.userid).where(Users.email == session['username']).all()
    user_id = user_id[0][0]
    # Render your monthly_calendar.html template
    new_tasks = db.session.query(Tasks.task_id, Tasks.task_name, Tasks.task_details, Tasks.task_duration, Tasks.deadline, Tasks.start_time, Tasks.end_time, Activities.activity_name, Activities.color).join(Activities, (Tasks.activity_id == Activities.activity_id)).where(Tasks.userid == user_id).order_by(func.age(Tasks.end_time).desc()).all()
    new_activities = db.session.query(Activities.activity_id, Activities.activity_name, Activities.activity_details, Activities.start_time, Activities.end_time, Activities.color).where(Tasks.userid == user_id).order_by(func.age(Activities.start_time).desc()).all()
    return render_template('monthly_calendar.html', activities=new_activities, tasks = new_tasks)

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if session:
        user_id = db.session.query(Users.userid).where(Users.email == session['username']).all()
        user_id = user_id[0][0]
    activities = db.session.query(Activities.activity_id, Activities.activity_name, Activities.activity_details, Activities.start_time, Activities.end_time).where(Activities.userid == user_id).order_by(func.age(Activities.start_time).asc()).all()
    if request.method == 'POST':
        print((request.form['task_name']))
        print((request.form['details']))
        print((request.form['activity']))
        print((request.form['deadline']))
        print(request.form['duration_hrs'])
        print(request.form['duration_mins'])
        task_name = request.form['task_name']
        task_details = request.form['details']
        task_duration = int(request.form['duration_hrs']) * 3600 + int((request.form['duration_mins'])) * 60
        print(task_duration)
        deadline = request.form['deadline']
        end_time = request.form['deadline']
        format_data = '%Y-%m-%dT%H:%M'
        id = db.session.query(Activities.activity_id).where(Activities.activity_name == request.form['activity']).all()
        if id[0][0]:
            activity_id = id[0][0]
            print(activity_id)
        uid = db.session.query(Users.userid).where(Users.email == session['username']).all()
        if uid[0][0]:
            user_id = uid[0][0]
            print(user_id)

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
            # flash('Task added successfully!')
            return jsonify({'message': 'Task added successfully!'}), 200
            # message = "Task added successfully!"
            #return render_template('add_task.html')

        except Exception as e:
            db.session.rollback()
            if (type(e).__name__) == "IntegrityError":
                message = "An internal error occured. \nPlease try again."
            if (type(e).__name__) == "ValueError":
                message = "An invalid datetime value was entered. \nPlease select a date from the dropdown calendar."
            # message = "An error occurred: {}".format(str(e))
            # flash(message)
            #return render_template('add_task.html')
            return jsonify({'message': message}), 400
    return render_template('add_task.html', activities = activities)

@app.route('/delete_task', methods=['POST'])
def delete_task():
    if request.method == 'POST':
        data = request.get_json()
        task_id = data.get('task_id')
        uid = db.session.query(Users.userid).where(Users.email == session['username']).one()
        print(uid[0], task_id)
        db.session.query(Tasks).filter(Tasks.userid == uid[0], Tasks.task_id == task_id).delete()
        #db.execute(text(f'DELETE FROM tasks WHERE task_id = 3 AND userid = 1'))
        db.session.commit()

        return jsonify({'message': 'Endpoint hit'}), 200

@app.route('/add_activity', methods=['GET', 'POST'])
def add_activity():
    if request.method == 'POST':
        format_data = '%Y-%m-%dT%H:%M'
        print((request.form['activity_name']))
        print((request.form['details']))
        print((request.form['start_time']))
        print((request.form['end_time']))
        activity_name = request.form['activity_name']
        activity_details = request.form['details']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        color = request.form['color']
        print(color)
        uid = db.session.query(Users.userid).where(Users.email == session['username']).one()
        if uid[0]:
            user_id = uid[0]
            print(user_id)

        try:
            new_activity = Activities(
                userid=user_id, 
                activity_name=activity_name,
                activity_details=activity_details,
                start_time = datetime.strptime(start_time, format_data),
                end_time = datetime.strptime(end_time, format_data),
                color = str(color)
            )
            db.session.add(new_activity)
            db.session.commit()
            # flash('Activity added successfully!')
            # message = "Task added successfully!"
            return jsonify({'message': 'Task added successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            if (type(e).__name__) == "IntegrityError":
                message = "An internal error occured. \nPlease try again."
            if (type(e).__name__) == "ValueError":
                message = "An invalid datetime value was entered. \nPlease select a date from the dropdown calendar."
                # message = "An error occurred: {}".format(str(e))
            else:
                message = "Error"
            #flash(message)
            return jsonify({'message': message}), 400
    return render_template('add_activity.html')

if __name__ == '__main__':
    app.run(debug=True)
