from werkzeug.security import generate_password_hash, check_password_hash

from app import db

# For the many-to-many relationship between subjects and students.
# One student can minor in several subjects and one subject can
# be taught to several students as a minor
student_subject_table = db.Table(
    "student_subject", db.Model.metadata,
    db.Column("student_id", db.String, db.ForeignKey("students.student_id")),
    db.Column("subject_id", db.String, db.ForeignKey("subjects.subject_id"))
)


class Person(db.Model):

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email_address = db.Column(db.String(255), unique=True, primary_key=True)
    password_hash = db.Column(db.String(128))
    person_type = db.Column(db.String(50))

    __mapper_args__ = {
        "polymorphic_identity": "person",
        "polymorphic_on": person_type
    }

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
        return "<Person: {} {}>".format(self.first_name, self.last_name)


class Student(Person):

    __tablename__ = "students"

    email_address = db.Column(db.String(255), db.ForeignKey(
                                "person.email_address"))
    student_id = db.Column(db.String, unique=True, primary_key=True)
    major_id = db.Column(db.String, db.ForeignKey("subjects.subject_id"))
    minors = db.relationship("Subject", secondary=student_subject_table,
                             back_populates="minor_students")
    __mapper_args__ = {
        "polymorphic_identity": "students",
    }

    def __repr__(self):
        return "<Student ID: {}>".format(self.student_id)


class Teacher(Person):

    __tablename__ = "teachers"

    email_address = db.Column(db.String(255), db.ForeignKey(
                                "person.email_address"))
    staff_id = db.Column(db.String, unique=True, primary_key=True)
    subjects_taught = db.relationship("Subject", backref="teacher",
                                      lazy="dynamic")
    __mapper_args__ = {
        "polymorphic_identity": "teachers",
    }

    def __repr__(self):
        return "<Staff ID: {}>".format(self.staff_id)


class Subject(db.Model):

    __tablename__ = "subjects"

    subject_id = db.Column(db.String, unique=True, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(150))
    teacher_id = db.Column(db.String, db.ForeignKey("teachers.staff_id"))
    major_students = db.relationship("Student", backref="major",
                                     lazy="dynamic")
    minor_students = db.relationship("Student",
                                     secondary=student_subject_table,
                                     back_populates="minors")

    def __repr__(self):
        return "<Subject ID: {}>".format(self.subject_id)
