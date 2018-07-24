import json

from tests import TestBase


class TestSubjects(TestBase):
    """Test /subjects endpoint
    """

    def test_list_subjects(self):
        """Test that listing all subjects is successful
        """
        response = self.app.get("/api/v1/subjects", headers=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertIn("subjects", response.data.decode('utf-8'))
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("Discrete Maths", output["subjects"][0]["name"])
        self.assertEqual("Introduction to discrete mathematics",
                         output["subjects"][0]["description"])

    def test_create_subject(self):
        """Test successful creation of subject
        """
        self.subject = {"subject_id": "SB002",
                        "name": "Literature",
                        "description": "Introduction to english literature"}
        response = self.app.post("/api/v1/subjects",
                                 data=self.subject,
                                 headers=self.token)
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data.decode('utf-8'))
        self.assertTrue("You have successfully created a new subject"
                        in output["message"])

    def test_missing_field(self):
        """Test that adding a new subject is unsuccessful if
        a required field is missing
        """

        self.subject = {"subject_id": "SB002",
                        "description": "Introduction to english literature"}
        response = self.app.post("/api/v1/subjects",
                                 data=self.subject,
                                 headers=self.token)
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data.decode('utf-8'))
        expected_response = {"description": "Please enter a description."}
        self.assertEqual(expected_response, output["message"])


class TestSubject(TestBase):
    """
    Test /subjects/<str:id> endpoint
    """

    def test_get_subject(self):
        """
        Test that one can see details of selected subject
        """
        response = self.app.get("/api/v1/subjects/SB001", headers=self.token)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("Discrete Maths", output["name"])
        self.assertEqual("Introduction to discrete mathematics",
                         output["description"])

    def test_nonexistent_id(self):
        """
        Test that trying to get a subject with a
        non-existent ID will be unsuccessful
        """
        response = self.app.get("/api/v1/subjects/SB123", headers=self.token)
        self.assertEqual(response.status_code, 404)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output, {"error": "A subject with ID SB123 "
                                  "does not exist."})

    def test_update_subject(self):
        """Test that one can update a selected subject.
        Test that only updated fields change while the
        rest remain the same.
        """
        self.subject = {"description": "New description"}
        response = self.app.put("/api/v1/subjects/SB001",
                                data=self.subject,
                                headers=self.token)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("You have successfully edited the subject.",
                         output["message"])
        self.assertEqual("Discrete Maths", output["name"])
        self.assertEqual("New description", output["description"])

    def test_delete_subject(self):
        """Test that one can delete a selected subject.
        """
        response = self.app.delete("/api/v1/subjects/SB001",
                                   headers=self.admin_token)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output, {"message": "You have successfully "
                         "deleted the subject with the following ID: SB001."})
