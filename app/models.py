from werkzeug.security import generate_password_hash, check_password_hash

from app import db

# For the many-to-many relationship between subjects and students.
# One student can minor in several subjects and one subject can
# be taught to several students as a minor
student_subject_table = db.Table(
    "student_subject", db.Model.metadata,
    db.Column("student_id", db.Integer, db.ForeignKey("students.id")),
    db.Column("subject_id", db.Integer, db.ForeignKey("subjects.id"))
)


class Person(db.Model):

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email_address = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(128))

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

    def __repr__(self):
        return "<Person {}: {} {}>".format(self.id, self.first_name,
                                           self.last_name)


class Student(Person):

    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    major_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    minors = db.relationship("Subject", secondary=student_subject_table,
                             back_populates="minor_students")


class Teacher(Person):

    __tablename__ = "teachers"

    staff_id = db.Column(db.Integer, primary_key=True)
    subjects_taught = db.relationship("Subject", backref="teacher",
                                      lazy="dynamic")


class Subject(db.Model):

    __tablename__ = "subjects"

    subject_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(150))
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    major_students = db.relationship("Student", backref="major",
                                     lazy="dynamic")
    minor_students = db.relationship("Student", secondary=student_subject_table,
                                     back_populates="minors")
