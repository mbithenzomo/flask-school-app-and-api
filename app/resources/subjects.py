import random

from flask import request
from flask_restful import Resource, reqparse, marshal

from app.resources import create_or_update_resource, delete_resource
from app.models import Subject, Teacher
from app.serializers import subject_serializer


class SubjectListAPI(Resource):
    """View all subjects; add new subject
    URL: /api/v1/subjects
    Request methods: POST, GET
    """

    def get(self):

        args = request.args.to_dict()
        page = int(args.get("page", 1))
        limit = int(args.get("limit", 20))
        kwargs = {}

        subjects = Subject.query.filter_by(**kwargs).paginate(
                             page=page, per_page=limit, error_out=False)
        page_count = subjects.pages
        has_next = subjects.has_next
        has_previous = subjects.has_prev
        if has_next:
            next_page = str(request.url_root) + "api/v1.0/subjects?" + \
                "limit=" + str(limit) + "&page=" + str(page + 1)
        else:
            next_page = "None"
        if has_previous:
            previous_page = request.url_root + "api/v1.0/subjects?" + \
                "limit=" + str(limit) + "&page=" + str(page - 1)
        else:
            previous_page = "None"
        subjects = subjects.items

        output = {"subjects": marshal(subjects, subject_serializer),
                  "has_next": has_next,
                  "page_count": page_count,
                  "previous_page": previous_page,
                  "next_page": next_page
                  }

        if subjects:
            return output
        else:
            return {"error": "There are no registered subjects. "
                             "Add a new one and try again!"}, 404

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument(
            "name",
            required=True,
            help="Please enter a name.")
        parser.add_argument(
            "description",
            required=True,
            help="Please enter a description.")
        parser.add_argument(
            "teacher_id",
            required=True,
            help="Please enter a valid teacher's ID.")
        args = parser.parse_args()
        name, description, teacher_id = args["name"], args["description"], \
            args["teacher_id"]
        subject = Subject(name=name,
                          description=description,
                          subject_id="SB" + str(random.randint(1, 999)))

        if teacher_id:
            teacher = Teacher.query.filter_by(staff_id=teacher_id).first()
            if not teacher:
                return {"error": "The teacher ID you entered is invalid."},
                400
            else:
                subject.teacher = teacher

        return create_or_update_resource(
            resource=subject,
            resource_type="subject",
            serializer=subject_serializer,
            create=True)


class SubjectAPI(Resource):
    """View, update and delete a single subject.
    URL: /api/v1/subjects/<id>
    Request methods: GET, PUT, DELETE
    """

    def get(self, id):

        subject = Subject.query.filter_by(subject_id=id).first()
        if subject:
            return marshal(subject, subject_serializer)
        else:
            return {"error": "A subject with ID " + id + " does "
                             "not exist."}, 404

    def put(self, id):

        subject = Subject.query.filter_by(subject_id=id).first()
        if subject:
            parser = reqparse.RequestParser()
            parser.add_argument("name")
            parser.add_argument("description")
            parser.add_argument("teacher_id")
            args = parser.parse_args()

            for field in args:
                if args[field] is not None:
                    if field == "teacher_id":
                        teacher_id = args["teacher_id"]
                        if teacher_id.startswith("TC"):
                            teacher = Teacher.query.filter_by(
                                staff_id=teacher_id).first()
                            if not teacher:
                                return {"error": "The teacher ID you entered "
                                        "is invalid."}, 400
                        else:
                            args["teacher_id"] = None
                    updated_field = args[field]
                    setattr(subject, field, updated_field)

            return create_or_update_resource(
                resource=subject,
                resource_type="subject",
                serializer=subject_serializer,
                create=False)
        else:
            return {"error": "A subject with ID " + id + " does "
                             "not exist."}, 404

    def delete(self, id):

        subject = Subject.query.filter_by(subject_id=id).first()
        if subject:
            return delete_resource(resource=subject,
                                   resource_type="subject",
                                   id=id)
        else:
            return {"error": "A subject with ID " + id + " does "
                             "not exist."}, 404
