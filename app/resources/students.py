import random

from flask import request
from flask_restful import Resource, reqparse, marshal

from app.resources import create_or_update_resource, delete_resource
from app.models import Student, Subject
from app.serializers import student_serializer


class StudentListAPI(Resource):
    """View all students; add new student
    URL: /api/v1/students
    Request methods: POST, GET
    """

    def get(self):

        args = request.args.to_dict()
        page = int(args.get("page", 1))
        limit = int(args.get("limit", 20))
        kwargs = {}

        students = Student.query.filter_by(**kwargs).paginate(
                             page=page, per_page=limit, error_out=False)
        page_count = students.pages
        has_next = students.has_next
        has_previous = students.has_prev
        if has_next:
            next_page = str(request.url_root) + "api/v1.0/students?" + \
                "limit=" + str(limit) + "&page=" + str(page + 1)
        else:
            next_page = "None"
        if has_previous:
            previous_page = request.url_root + "api/v1.0/students?" + \
                "limit=" + str(limit) + "&page=" + str(page - 1)
        else:
            previous_page = "None"
        students = students.items

        output = {"students": marshal(students, student_serializer),
                  "has_next": has_next,
                  "page_count": page_count,
                  "previous_page": previous_page,
                  "next_page": next_page
                  }

        if students:
            return output
        else:
            return {"error": "There are no registered students. "
                             "Add a new one and try again!"}, 404

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument(
            "first_name",
            required=True,
            help="Please enter a first name.")
        parser.add_argument(
            "last_name",
            required=True,
            help="Please enter a last name.")
        parser.add_argument(
            "email_address",
            required=True,
            help="Please enter an email address.")
        parser.add_argument(
            "major_id",
            help="Please enter only one subject ID.")
        parser.add_argument(
            "minors",
            help="Separate multiple subject IDs with a comma.")
        args = parser.parse_args()
        first_name, last_name, email_address, major_id, minors = \
            args["first_name"], args["last_name"], args["email_address"], \
            args["major_id"], args["minors"]
        student = Student(first_name=first_name,
                          last_name=last_name,
                          email_address=email_address,
                          student_id="ST" + str(random.randint(1, 999)))

        if major_id:
            student.major_id = major_id

        if minors:
            minors_list = [minor.strip() for minor in minors.split(',')]
            for subject_id in minors_list:
                try:
                    minor = Subject.query.get(subject_id)
                    if minor:
                        student.minors.append(minor)
                    else:
                        return {"error": "One or more minor subject IDs you "
                                "entered is invalid."}, 400
                except:
                    return {"error": "The minors field should only contain "
                            "integers separated by a comma."}, 400
        return create_or_update_resource(
            resource=student,
            resource_type="student",
            serializer=student_serializer,
            create=True)


class StudentAPI(Resource):
    """View, update and delete a single student.
    URL: /api/v1/students/<id>
    Request methods: GET, PUT, DELETE
    """

    def get(self, id):

        student = Student.query.filter_by(student_id=id).first()
        if student:
            return marshal(student, student_serializer)
        else:
            return {"error": "A student with ID " + id + " does "
                             "not exist."}, 404

    def put(self, id):

        student = Student.query.filter_by(student_id=id).first()
        if student:
            parser = reqparse.RequestParser()
            parser.add_argument("first_name")
            parser.add_argument("last_name")
            parser.add_argument("email_address")
            parser.add_argument("major_id")
            parser.add_argument("minors")
            args = parser.parse_args()

            for field in args:
                if args[field] is not None:
                    if field == "minors":
                        # Clear the student's list of minors
                        for subject in student.minors:
                            subject.minor_students.remove(student)
                        student.minors = []
                        minors = args["minors"]
                        minors_list = [minor.strip() for minor in
                                       minors.split(',')]
                        # Append new minors into list
                        if minors_list != [u'']:
                            for subject_id in minors_list:
                                try:
                                    minor = Subject.query.get(subject_id)
                                    if minor:
                                        student.minors.append(minor)
                                    else:
                                        return {"error": "One or more subject "
                                                "IDs you entered is "
                                                "invalid."}, 400
                                except:
                                    return {"error": "The minors field should "
                                            "only contain subject IDs "
                                            "separated by a comma."}, 400
                    elif field == "email_address":
                        return {"error": "You can't update the email address "
                                "field."}, 400
                    else:
                        updated_field = args[field]
                        setattr(student, field, updated_field)
        else:
            return {"error": "A student with ID " + id + " does "
                             "not exist."}, 404

        return create_or_update_resource(
            resource=student,
            resource_type="student",
            serializer=student_serializer,
            create=False)

    def delete(self, id):

        student = Student.query.filter_by(student_id=id).first()
        if student:
            return delete_resource(resource=student,
                                   resource_type="student",
                                   id=id)
        else:
            return {"error": "A student with ID " + id + " does "
                             "not exist."}, 404
