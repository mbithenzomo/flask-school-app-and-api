import json
import os
import requests

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app import app, db
from app.models import Student, Teacher, Subject, User

if os.getenv("ENVIRONMENT") == "development":
    path = "http://127.0.0.1:5000"
else:
    path = "https://flask-school-app.herokuapp.com"


def create_admin_user():
    admin = User.query.filter_by(username="admin").first()
    if admin:
        db.session.delete(admin)
        db.session.commit()

    admin = User(username="admin",
                 password="admin1234")
    db.session.add(admin)
    db.session.commit()


def get_token():
    admin = {"username": "admin",
             "password": "admin1234"}
    response = requests.post(path + "/api/v1/auth/login",
                             data=admin)
    output = json.loads(response.text)
    token = output["token"]
    return {"Authorization": token}


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    print links
    return render_template('login.html', title='Login')


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = {"username": request.form["username"],
                "password": request.form["password"]}
        response = requests.post(path + "/api/v1/auth/login",
                                 data=user)
        output = json.loads(response.text)
        if output.get("error"):
            error = output["error"]
        else:
            admin_user_id = output.get("user_id")
            admin_user = User.query.get(int(admin_user_id))
            login_user(admin_user)
            return redirect(url_for('dashboard'))

    return render_template('login.html', title='Login', error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    message = "Successfully logged out."
    return render_template('login.html', title='Login', message=message)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    students = Student.query.all()
    teachers = Teacher.query.all()
    subjects = Subject.query.all()
    return render_template('dashboard.html', title='Dashboard',
                           students=students, teachers=teachers,
                           subjects=subjects)


@app.route('/add-student', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        create_admin_user()
        student = {"first_name": request.form["first_name"],
                   "last_name": request.form["last_name"],
                   "email_address": request.form["email_address"],
                   "major_id": request.form["major"],
                   "minors": request.form["minors"]}
        response = requests.post(path + "/api/v1/students",
                                 data=student,
                                 headers=get_token())
        output = json.loads(response.text)
        if output.get("error"):
            flash(output["error"], "error")
        else:
            if "error" in output["message"].lower():
                flash(output["message"], "error")
            else:
                flash(output["message"], "success")

        return redirect(url_for('dashboard'))


@app.route('/edit-student/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Student.query.filter_by(student_id=id).first()
    if student:
        if request.method == 'POST':
            create_admin_user()
            student = {"first_name": request.form["first_name"],
                       "last_name": request.form["last_name"],
                       "major_id": request.form["major"],
                       "minors": request.form["minors"]}
            response = requests.put(path + "/api/v1/students/" + id,
                                    data=student,
                                    headers=get_token())
            output = json.loads(response.text)
            if output.get("error"):
                flash(output["error"], "error")
            else:
                if "error" in output["message"].lower():
                    flash(output["message"], "error")
                else:
                    flash(output["message"], "success")
    else:
        flash("Specified student doesn't exit!", "error")

    return redirect(url_for('dashboard'))


@app.route('/delete-student/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_student(id):
    student = Student.query.filter_by(student_id=id).first()
    if student:
        create_admin_user()
        response = requests.delete(path + "/api/v1/students/" + id,
                                   headers=get_token())
        output = json.loads(response.text)
        if output.get("error"):
            flash(output["error"], "error")
        else:
            if "error" in output["message"].lower():
                flash(output["message"], "error")
            else:
                flash(output["message"], "success")
    else:
        flash("Specified student doesn't exit!", "error")

    return redirect(url_for('dashboard'))


@app.route('/add-teacher', methods=['GET', 'POST'])
@login_required
def add_teacher():
    if request.method == 'POST':
        create_admin_user()
        teacher = {"first_name": request.form["first_name"],
                   "last_name": request.form["last_name"],
                   "email_address": request.form["email_address"],
                   "subjects_taught": request.form["subjects_taught"]}
        response = requests.post(path + "/api/v1/teachers",
                                 data=teacher,
                                 headers=get_token())
        output = json.loads(response.text)
        if output.get("error"):
            flash(output["error"], "error")
        else:
            if "error" in output["message"].lower():
                flash(output["message"], "error")
            else:
                flash(output["message"], "success")

        return redirect(url_for('dashboard'))


@app.route('/edit-teacher/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(id):
    teacher = Teacher.query.filter_by(staff_id=id).first()
    if teacher:
        if request.method == 'POST':
            create_admin_user()
            teacher = {"first_name": request.form["first_name"],
                       "last_name": request.form["last_name"],
                       "subjects_taught": request.form["subjects_taught"]}
            response = requests.put(path + "/api/v1/teachers/" + id,
                                    data=teacher,
                                    headers=get_token())
            output = json.loads(response.text)
            if output.get("error"):
                flash(output["error"], "error")
            else:
                if "error" in output["message"].lower():
                    flash(output["message"], "error")
                else:
                    flash(output["message"], "success")
    else:
        flash("Specified teacher doesn't exit!", "error")

    return redirect(url_for('dashboard'))


@app.route('/delete-teacher/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_teacher(id):
    teacher = Teacher.query.filter_by(staff_id=id).first()
    if teacher:
        create_admin_user()
        response = requests.delete(path + "/api/v1/teachers/" + id,
                                   headers=get_token())
        output = json.loads(response.text)
        if output.get("error"):
            flash(output["error"], "error")
        else:
            if "error" in output["message"].lower():
                flash(output["message"], "error")
            else:
                flash(output["message"], "success")
    else:
        flash("Specified teacher doesn't exit!", "error")

    return redirect(url_for('dashboard'))


@app.route('/add-subject', methods=['GET', 'POST'])
@login_required
def add_subject():
    if request.method == 'POST':
        create_admin_user()
        subject = {"name": request.form["name"],
                   "description": request.form["description"],
                   "teacher_id": request.form["teacher_id"]}
        response = requests.post(path + "/api/v1/subjects",
                                 data=subject,
                                 headers=get_token())
        output = json.loads(response.text)
        if output.get("error"):
            flash(output["error"], "error")
        else:
            if "error" in output["message"].lower():
                flash(output["message"], "error")
            else:
                flash(output["message"], "success")

        return redirect(url_for('dashboard'))


@app.route('/edit-subject/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_subject(id):
    subject = Subject.query.filter_by(subject_id=id).first()
    if subject:
        if request.method == 'POST':
            create_admin_user()
            subject = {"name": request.form["name"],
                       "description": request.form["description"],
                       "teacher_id": request.form["teacher_id"]}
            response = requests.put(path + "/api/v1/subjects/" + id,
                                    data=subject,
                                    headers=get_token())
            output = json.loads(response.text)
            if output.get("error"):
                flash(output["error"], "error")
            else:
                if "error" in output["message"].lower():
                    flash(output["message"], "error")
                else:
                    flash(output["message"], "success")
    else:
        flash("Specified subject doesn't exit!", "error")

    return redirect(url_for('dashboard'))


@app.route('/delete-subject/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_subject(id):
    subject = Subject.query.filter_by(subject_id=id).first()
    if subject:
        create_admin_user()
        response = requests.delete(path + "/api/v1/subjects/" + id,
                                   headers=get_token())
        output = json.loads(response.text)
        if output.get("error"):
            flash(output["error"], "error")
        else:
            if "error" in output["message"].lower():
                flash(output["message"], "error")
            else:
                flash(output["message"], "success")
    else:
        flash("Specified subject doesn't exit!", "error")

    return redirect(url_for('dashboard'))
