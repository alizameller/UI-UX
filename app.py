from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Placeholder data for demonstration
tasks = [
    {"id": 1, "activity": "UI/UX", "name": "Homework", "details": "Details of Task 1", "start_time": "2024-04-01T15:40", "end_time": "2024-04-01T17:00", "priority": "High"},
    {"id": 2, "activity": "Databases", "name": "Presentation", "details": "Details of Task 2", "start_time": "2024-04-02T12:40", "end_time": "2024-04-02T15:00", "priority": "Medium"},
    {"id": 3, "activity": "Senior Projects", "name": "Meeting", "details": "Details of Task 2", "start_time": "2024-04-02T12:40", "end_time": "2024-04-02T15:00", "priority": "Medium"},
    {"id": 4, "activity": "Databases", "name": "Assignment", "details": "Details of Task 2", "start_time": "2024-04-03T12:40", "end_time": "2024-04-03T15:00", "priority": "Medium"},
    {"id": 5, "activity": "UI/UX", "name": "Assignment", "details": "Details of Task 2", "start_time": "2024-04-03T12:40", "end_time": "2024-04-03T15:00", "priority": "Medium"},
]

colors = {"Databases": "rgb(226, 0, 246)", "UI/UX": "rgb(73, 246, 250)"}

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
    return render_template('monthly_calendar.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')

if __name__ == '__main__':
    app.run(debug=True)
