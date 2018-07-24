import nose2

from flask_testing import TestCase

from app import db
from app.models import Student, Teacher, Subject
from config.config import app_config
from run import app

app.config.from_object(app_config["testing"])


class TestBase(TestCase):
    """ Base configurations for the tests """

    def create_app(self):
        """Create Flask app
        """
        return app

    def get_token(self):
        """Return authentication token
        """
        pass

    def setUp(self):
        """Set up test client and populate test database with test data
        """
        self.app = app.test_client()
        student = Student(student_id="ST001",
                          first_name="Jane",
                          last_name="Doe",
                          email_address="jane.doe@school.edu",
                          password="pass1234")
        teacher = Teacher(staff_id="TC001",
                          first_name="Johnny",
                          last_name="Walker",
                          email_address="johnny.walker@school.edu",
                          password="pass1234")
        subject = Subject(subject_id="SB001",
                          name="Discrete Maths",
                          description="Introduction to discrete mathematics")

        subject.major_students.append(student)
        teacher.subjects_taught.append(subject)

        db.session.add(student)
        db.session.add(teacher)
        db.session.add(subject)

        self.token = self.get_token()

    def tearDown(self):
        """Destroy test database"""
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    nose2.run()
