import random

from flask import request
from flask_restful import Resource, reqparse, marshal

from app.resources import create_or_update_resource, delete_resource
from app.models import Teacher, Subject
from app.serializers import teacher_serializer


class TeacherListAPI(Resource):
    """View all teachers; add new teacher
    URL: /api/v1/teachers
    Request methods: POST, GET
    """

    def get(self):

        args = request.args.to_dict()
        page = int(args.get("page", 1))
        limit = int(args.get("limit", 20))
        kwargs = {}

        teachers = Teacher.query.filter_by(**kwargs).paginate(
                             page=page, per_page=limit, error_out=False)
        page_count = teachers.pages
        has_next = teachers.has_next
        has_previous = teachers.has_prev
        if has_next:
            next_page = str(request.url_root) + "api/v1.0/teachers?" + \
                "limit=" + str(limit) + "&page=" + str(page + 1)
        else:
            next_page = "None"
        if has_previous:
            previous_page = request.url_root + "api/v1.0/teachers?" + \
                "limit=" + str(limit) + "&page=" + str(page - 1)
        else:
            previous_page = "None"
        teachers = teachers.items

        output = {"teachers": marshal(teachers, teacher_serializer),
                  "has_next": has_next,
                  "page_count": page_count,
                  "previous_page": previous_page,
                  "next_page": next_page
                  }

        if teachers:
            return output
        else:
            return {"error": "There are no registered teachers. "
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
            "subjects_taught",
            help="Separate multiple subject IDs with a comma.")
        args = parser.parse_args()
        first_name, last_name, email_address, subjects_taught = \
            args["first_name"], args["last_name"], args["email_address"], \
            args["subjects_taught"]
        teacher = Teacher(first_name=first_name,
                          last_name=last_name,
                          email_address=email_address,
                          staff_id="TC" + str(random.randint(1, 999)))
        if subjects_taught:
            subjects_taught_list = [subject.strip() for subject in
                                    subjects_taught.split(',')]
            for subject_id in subjects_taught_list:
                try:
                    subject = Subject.query.get(subject_id)
                    if subject:
                        teacher.subjects_taught.append(subject)
                    else:
                        return {"error": "One or more subject IDs you entered "
                                "is invalid."}, 400
                except:
                    return {"error": "The subjects_taught field should only "
                            "contain subject IDs separated by a comma."}, 400
        return create_or_update_resource(
            resource=teacher,
            resource_type="teacher",
            serializer=teacher_serializer,
            create=True)


class TeacherAPI(Resource):
    """View, update and delete a single teacher.
    URL: /api/v1/teachers/<id>
    Request methods: GET, PUT, DELETE
    """

    def get(self, id):

        teacher = Teacher.query.filter_by(staff_id=id).first()
        if teacher:
            return marshal(teacher, teacher_serializer)
        else:
            return {"error": "A teacher with ID " + id + " does "
                             "not exist."}, 404

    def put(self, id):

        teacher = Teacher.query.filter_by(staff_id=id).first()
        if teacher:
            parser = reqparse.RequestParser()
            parser.add_argument("first_name")
            parser.add_argument("last_name")
            parser.add_argument("email_address")
            parser.add_argument("subjects_taught")
            args = parser.parse_args()

            for field in args:
                if args[field] is not None:
                    if field == "subjects_taught":
                        # Clear the teacher's list of subjects
                        for subject in teacher.subjects_taught:
                            subject.teacher = None
                        teacher.subjects_taught = []
                        subjects_taught = args["subjects_taught"]
                        subjects_taught_list = [subject.strip() for subject in
                                                subjects_taught.split(',')]
                        # Append new subjects into list
                        if subjects_taught_list != [u'']:
                            for subject_id in subjects_taught_list:
                                try:
                                    subject = Subject.query.get(subject_id)
                                    if subject:
                                        teacher.subjects_taught.append(subject)
                                    else:
                                        return {"error": "One or more subject "
                                                "IDs you entered is invalid."},
                                        400
                                except:
                                    return {"error": "The subjects_taught "
                                            "field should only contain "
                                            "subject IDs separated by a "
                                            "comma."}, 400
                    elif field == "email_address":
                        return {"error": "You can't update the email address "
                                "field."}, 400
                    else:
                        updated_field = args[field]
                        setattr(teacher, field, updated_field)

            return create_or_update_resource(
                resource=teacher,
                resource_type="teacher",
                serializer=teacher_serializer,
                create=False)
        else:
            return {"error": "A teacher with ID " + id + " does "
                             "not exist."}, 404

    def delete(self, id):

        teacher = Teacher.query.filter_by(staff_id=id).first()
        if teacher:
            return delete_resource(resource=teacher,
                                   resource_type="teacher",
                                   id=id)
        else:
            return {"error": "A teacher with ID " + id + " does "
                             "not exist."}, 404
