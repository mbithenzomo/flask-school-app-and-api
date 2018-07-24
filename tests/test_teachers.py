import json

from tests import TestBase


class TestTeachers(TestBase):
    """Test /teachers endpoint
    """

    def test_list_teachers(self):
        """Test that listing all teachers is successful
        """
        response = self.app.get("/api/v1/teachers", headers=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertIn("teachers", response.data.decode('utf-8'))
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("Minerva", output["teachers"][0]["first_name"])
        self.assertEqual("McGonagall", output["teachers"][0]["last_name"])

    def test_create_teacher(self):
        """Test successful creation of teacher
        """
        self.teacher = {"teacher_id": "TC002",
                        "first_name": "Severus",
                        "last_name": "Snape",
                        "email_address": "severus.snape@hogwarts.edu"}
        response = self.app.post("/api/v1/teachers",
                                 data=self.teacher,
                                 headers=self.token)
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data.decode('utf-8'))
        self.assertTrue("You have successfully created a new teacher"
                        in output["message"])

    def test_missing_field(self):
        """Test that adding a new teacher is unsuccessful if
        a required field is missing
        """

        self.teacher = {"teacher_id": "TC002",
                        "first_name": "Severus",
                        "last_name": "Snape"}
        response = self.app.post("/api/v1/teachers",
                                 data=self.teacher,
                                 headers=self.token)
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data.decode('utf-8'))
        expected_response = {"email_address": "Please enter an email address."}
        self.assertEqual(expected_response, output["message"])


class TestTeacher(TestBase):
    """
    Test /teachers/<str:id> endpoint
    """

    def test_get_teacher(self):
        """
        Test that one can see details of selected teacher
        """
        response = self.app.get("/api/v1/teachers/TC001", headers=self.token)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("Minerva", output["first_name"])
        self.assertEqual("McGonagall", output["last_name"])

    def test_nonexistent_id(self):
        """
        Test that trying to get a teacher with a
        non-existent ID will be unsuccessful
        """
        response = self.app.get("/api/v1/teachers/TC123", headers=self.token)
        self.assertEqual(response.status_code, 404)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output, {"error": "A teacher with ID TC123 "
                                  "does not exist."})

    def test_update_teacher(self):
        """Test that one can update a selected teacher.
        Test that only updated fields change while the
        rest remain the same.
        """
        self.teacher = {"first_name": "New first name"}
        response = self.app.put("/api/v1/teachers/TC001",
                                data=self.teacher,
                                headers=self.token)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("You have successfully edited the teacher",
                         output["message"])
        self.assertEqual("New first name", output["first_name"])
        self.assertEqual("McGonagall", output["last_name"])

    def test_delete_teacher(self):
        """Test that one can delete a selected teacher.
        """
        response = self.app.delete("/api/v1/teachers/TC001",
                                   headers=self.token)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output, {"message": "You have successfully "
                         "deleted the teacher with the following ID: TC001"})
