import json

import nose2

from flask_testing import TestCase

from app import db
from app.models import Student, Subject, Teacher, User
from config.config import app_config
from run import app

app.config.from_object(app_config["testing"])


class TestBase(TestCase):
    """Base configurations for the tests
    """

    def create_app(self):
        """Create Flask app
        """
        return app

    def get_token(self):
        """Returns authentication token
        """
        self.user = {"username": "testuser",
                     "password": "testpassword"}
        response = self.app.post("/api/v1/auth/login",
                                 data=self.user)
        output = json.loads(response.data.decode('utf-8'))
        token = output["token"].encode()
        return {"Authorization": token}

    def setUp(self):
        """Set up test client and populate test database with test data
        """
        self.app = app.test_client()
        db.create_all()
        user = User(username="testuser",
                    password="testpassword")
        student = Student(student_id="ST001",
                          first_name="Hermione",
                          last_name="Granger",
                          email_address="hermione.granger@hogwarts.edu")
        teacher = Teacher(staff_id="TC001",
                          first_name="Minerva",
                          last_name="McGonagall",
                          email_address="minerva.mcgonagall@hogwarts.edu")
        subject = Subject(subject_id="SB001",
                          name="Transfiguration",
                          description="Teaches the art of changing the form "
                          "and appearance of an object or a person.")

        subject.major_students.append(student)
        teacher.subjects_taught.append(subject)

        db.session.add(user)
        db.session.add(student)
        db.session.add(teacher)
        db.session.add(subject)

        self.token = self.get_token()

    def tearDown(self):
        """Destroy test database
        """
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    nose2.run()
