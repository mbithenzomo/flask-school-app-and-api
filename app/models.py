import jwt
import datetime as dt
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db, login_manager

# For the many-to-many relationship between subjects and students.
# One student can minor in several subjects and one subject can
# be taught to several students as a minor
student_subject_table = db.Table(
    "student_subject", db.Model.metadata,
    db.Column("student_id", db.String(50), db.ForeignKey(
        "students.student_id")),
    db.Column("subject_id", db.String(50), db.ForeignKey(
        "subjects.subject_id"))
)


class User(db.Model, UserMixin):
    """Users will be able to register and login.
    They will also get a token that will allow
    them to make requests.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    @property
    def password(self):
        """Prevents access to password property
        """
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        """Sets password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Checks if password matches
        """
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, user_id):
        """Generates the auth token and returns it
        """
        try:
            payload = {
                "exp": dt.datetime.now() + dt.timedelta(
                    days=0, seconds=180000),
                "iat": dt.datetime.now(),
                "sub": user_id
            }
            return jwt.encode(
                payload,
                app.config.get("SECRET_KEY"),
                algorithm="HS256"
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the auth token
        """
        try:
            payload = jwt.decode(auth_token, app.config.get("SECRET_KEY"),
                                 options={'verify_iat': False})
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

    def __repr__(self):
        return "<User: {}>".format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Person(db.Model):

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email_address = db.Column(db.String(255), unique=True, primary_key=True)
    person_type = db.Column(db.String(50))

    __mapper_args__ = {
        "polymorphic_identity": "person",
        "polymorphic_on": person_type
    }

    def __repr__(self):
        return "<{}: {} {}>".format(self.person_type, self.first_name,
                                    self.last_name)


class Student(Person):

    __tablename__ = "students"

    email_address = db.Column(db.String(255), db.ForeignKey(
                                "person.email_address"))
    student_id = db.Column(db.String(50), unique=True, primary_key=True)
    major_id = db.Column(db.String(50), db.ForeignKey("subjects.subject_id"))
    minors = db.relationship("Subject", secondary=student_subject_table,
                             back_populates="minor_students")
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    __mapper_args__ = {
        "polymorphic_identity": "students",
    }

    def __repr__(self):
        return "<Student ID: {}>".format(self.student_id)


class Teacher(Person):

    __tablename__ = "teachers"

    email_address = db.Column(db.String(255), db.ForeignKey(
                                "person.email_address"))
    staff_id = db.Column(db.String(50), unique=True, primary_key=True)
    subjects_taught = db.relationship("Subject", backref="teacher",
                                      lazy="dynamic")
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    __mapper_args__ = {
        "polymorphic_identity": "teachers",
    }

    def __repr__(self):
        return "<Staff ID: {}>".format(self.staff_id)


class Subject(db.Model):

    __tablename__ = "subjects"

    subject_id = db.Column(db.String(50), unique=True, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(150))
    teacher_id = db.Column(db.String(50), db.ForeignKey("teachers.staff_id"))
    major_students = db.relationship("Student", backref="major",
                                     lazy="dynamic")
    minor_students = db.relationship("Student",
                                     secondary=student_subject_table,
                                     back_populates="minors")
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    def __repr__(self):
        return "<Subject ID: {}>".format(self.subject_id)
