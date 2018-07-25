from flask_restful import fields

"""Defining how resources are represented
"""

teacher_serializer = {
    "staff_id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "email_address": fields.String,
    "created_at": fields.DateTime(dt_format='rfc822'),
    "updated_at": fields.DateTime(dt_format='rfc822')
}

subject_serializer = {
    "subject_id": fields.String,
    "name": fields.String,
    "description": fields.String,
    "teacher": fields.Nested(teacher_serializer),
    "created_at": fields.DateTime(dt_format='rfc822'),
    "updated_at": fields.DateTime(dt_format='rfc822')
}

student_serializer = {
    "student_id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "email_address": fields.String,
    "major": fields.Nested(subject_serializer),
    "minors": fields.Nested(subject_serializer),
    "created_at": fields.DateTime(dt_format='rfc822'),
    "updated_at": fields.DateTime(dt_format='rfc822')
}
