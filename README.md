[![Build Status](https://travis-ci.org/mbithenzomo/flask-student-api.svg?branch=develop)](https://travis-ci.org/mbithenzomo/flask-student-api)
![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)

# School API
This is a RESTful API with the following properties:

1. It has the following relational entities:
    1. Student
    2. Teacher
    3. Subject
2. Each student can have only one subject as a major, but can read any subject as well (minors)
3. A subject is taught by one teacher
4. It has endpoints to CREATE, UPDATE, and DELETE each entity in the application
5. Only an authorized user can access the endpoints

## Installation and Set Up
Clone the repo from GitHub:
```
git clone https://github.com/mbithenzomo/flask-student-api
```

Fetch from the develop branch:
```
git fetch origin develop
```

Navigate to the root folder:
```
cd flask-student-api
```

Install the required packages:
```
pip install -r requirements.txt
```

Initialize, migrate, and upgrade the database:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## Launching the Program
Run ```python run.py```. You may use [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en) for Google Chrome to run the API.

## API Endpoints

| Resource URL | Methods | Description | Requires Token |
| -------- | ------------- | --------- |--------------- |
| `/api/v1` | GET  | The index | FALSE |
| `/api/v1/auth/register` | POST  | User registration | FALSE |
|  `/api/v1/auth/login` | POST | User login | FALSE |
| `/api/v1/students` | GET, POST | View all students, add a student | TRUE |
| `/api/v1/students/<string:id>` | GET, PUT, DELETE | View, edit, and delete a single student | TRUE |
| `/api/v1/teachers` | GET, POST | View all teachers, add a teacher | TRUE |
| `/api/v1/teachers/<string:id>` | GET, PUT, DELETE | View, edit, and delete a single teacher | TRUE |
| `/api/v1/subjects` | GET, POST | View all subjects, add a subject | TRUE |
| `/api/v1/subjects/<string:id>` | GET, PUT, DELETE | View, edit, and delete a single subject | TRUE |


## Sample Requests

Registering and logging in to get a JWT token:
![User Registration](https://github.com/mbithenzomo/flask-bucketlist-api/blob/develop/screenshots/register_user.png)

![User Login](https://github.com/mbithenzomo/flask-bucketlist-api/blob/develop/screenshots/login_user.png)

Displaying a paginated list of teachers:
![List of Teachers](https://github.com/mbithenzomo/flask-bucketlist-api/blob/develop/screenshots/list_teachers.png)

Displaying a paginated list of subjects:
![List of Subjects](https://github.com/mbithenzomo/flask-bucketlist-api/blob/develop/screenshots/list_subjects.png)

Updating a student:
![Updating Student](https://github.com/mbithenzomo/flask-bucketlist-api/blob/develop/screenshots/update_student.png)

## Testing
To test, run the following command: ```nose2```

## Built With...
* [Flask](http://flask.pocoo.org/)
* [Flask-RESTful](http://flask-restful-cn.readthedocs.io/en/0.3.4/)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)

## Credits

Copyright (c) 2018 [Mbithe Nzomo](https://github.com/mbithenzomo)
