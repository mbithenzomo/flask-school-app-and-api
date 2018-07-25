import json

from tests import TestBase


class TestStudents(TestBase):
    """Test /students endpoint
    """

    def test_list_students(self):
        """Test that listing all students is successful
        """
        response = self.app.get("/api/v1/students", headers=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertIn("students", response.data.decode('utf-8'))
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("Hermione", output["students"][0]["first_name"])
        self.assertEqual("Granger", output["students"][0]["last_name"])

    def test_create_student(self):
        """Test successful creation of student
        """
        self.student = {"student_id": "ST002",
                        "first_name": "Ginny",
                        "last_name": "Weasley",
                        "email_address": "ginny.weasley@hogwarts.edu"}
        response = self.app.post("/api/v1/students",
                                 data=self.student,
                                 headers=self.token)
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data.decode('utf-8'))
        self.assertTrue("You have successfully created a new student"
                        in output["message"])

    def test_missing_field(self):
        """Test that adding a new student is unsuccessful if
        a required field is missing
        """

        self.student = {"student_id": "ST002",
                        "first_name": "Luna",
                        "email_address": "luna.lovegood@hogwarts.edu"}
        response = self.app.post("/api/v1/students",
                                 data=self.student,
                                 headers=self.token)
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data.decode('utf-8'))
        expected_response = {"last_name": "Please enter a last name."}
        self.assertEqual(expected_response, output["message"])


class TestStudent(TestBase):
    """
    Test /students/<string:id> endpoint
    """

    def test_get_student(self):
        """
        Test that one can see details of selected student
        """
        response = self.app.get("/api/v1/students/ST001", headers=self.token)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("Hermione", output["first_name"])
        self.assertEqual("Granger", output["last_name"])

    def test_nonexistent_id(self):
        """
        Test that trying to get a student with a
        non-existent ID will be unsuccessful
        """
        response = self.app.get("/api/v1/students/ST123", headers=self.token)
        self.assertEqual(response.status_code, 404)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output, {"error": "A student with ID ST123 "
                                  "does not exist."})

    def test_update_student(self):
        """Test that one can update a selected student.
        Test that only updated fields change while the
        rest remain the same.
        """
        self.student = {"last_name": "New last name"}
        response = self.app.put("/api/v1/students/ST001",
                                data=self.student,
                                headers=self.token)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("You have successfully edited the student",
                         output["message"])
        self.assertEqual("New last name", output["last_name"])
        self.assertEqual("Hermione", output["first_name"])

    def test_delete_student(self):
        """Test that one can delete a selected student.
        """
        response = self.app.delete("/api/v1/students/ST001",
                                   headers=self.token)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output, {"message": "You have successfully "
                         "deleted the student with the following ID: ST001"})
