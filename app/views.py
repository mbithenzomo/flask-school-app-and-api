import os
import requests

from ast import literal_eval

from flask import redirect, render_template, request, url_for

from app import app
from app.models import Student, Teacher, Subject

if os.getenv("ENVIRONMENT") == "development":
    path = "http://127.0.0.1:5000"
else:
    path = "https://flaskschoolapp.pythonanywhere.com"


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = {"username": request.form["username"],
                "password": request.form["password"]}
        response = requests.post(path + "/api/v1/auth/login",
                                 data=user)
        output = literal_eval(response.text.encode('utf-8'))
        if output.get("error"):
            error = output["error"]
        else:
            return redirect(url_for('dashboard'))

    return render_template('login.html', title='Login', error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    message = "Successfully logged out."
    return render_template('login.html', title='Login', message=message)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    students = Student.query.all()
    teachers = Teacher.query.all()
    subjects = Subject.query.all()
    return render_template('dashboard.html', title='Dashboard',
                           students=students, teachers=teachers,
                           subjects=subjects)
