import json

from tests import TestBase


class TestAuth(TestBase):

    def test_index(self):
        """
        Test response to the index route
        """
        response = self.app.get("/api/v1")
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output, {"message": "Welcome to the School API."})

    def test_no_token(self):
        """
        Test that users must provide a token to make requests
        to protected endpoints
        """
        response = self.app.get("/api/v1/students")
        self.assertEqual(response.status_code, 401)
        output = json.loads(response.data.decode('utf-8'))
        self.assertTrue("Please enter a token" in output["error"])

        response = self.app.get("/api/v1/teachers")
        self.assertEqual(response.status_code, 401)
        output = json.loads(response.data.decode('utf-8'))
        self.assertTrue("Please enter a token" in output["error"])

        response = self.app.get("/api/v1/subjects")
        self.assertEqual(response.status_code, 401)
        output = json.loads(response.data.decode('utf-8'))
        self.assertTrue("Please enter a token" in output["error"])

    def test_invalid_token(self):
        """
        Test that invalid tokens cannot be used for protected endpoints
        """
        response = self.app.get("/api/v1/students",
                                headers={"Authorization": "1234"})
        self.assertEqual(response.status_code, 401)
        output = json.loads(response.data.decode('utf-8'))
        self.assertTrue("Invalid token" in output["error"])
