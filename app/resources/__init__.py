from flask import g, jsonify, request

from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource, marshal
from sqlalchemy.exc import IntegrityError

from app import app, db
from app.models import User


def create_or_update_resource(**kwargs):
    """Add a resource to the database or update an existing resource.
    Also handles integrity errors.
    Arguments:
        kwargs["name"]: The name of the resource to be added to the database.
        kwargs["resource"]: The resource to be added to the database.
        kwargs["serializer"]: The marshal serializer.
        kwargs["create"]: Flag to determine whether resource is being created.
        kwargs["resource_type"]: The type of resource, e.g student, teacher.
    """
    try:
        db.session.add(kwargs["resource"])
        db.session.commit()

        if kwargs["create"]:
            if kwargs["resource_type"] == "user":
                # Get user's auth token
                user = User.query.filter_by(
                    username=kwargs["username"]).first()
                auth_token = user.generate_auth_token(user.id)

                response = {"message": "You have successfully signed up",
                            "token": auth_token.decode()}
            else:
                response = marshal(kwargs["resource"], kwargs["serializer"])
                message = {"message": "You have successfully created a new " +
                           kwargs["resource_type"]}
                response.update(message)
            return response, 201
        else:
            response = marshal(kwargs["resource"], kwargs["serializer"])
            message = {"message": "You have successfully edited the " +
                       kwargs["resource_type"]}
            response.update(message)
            return response

    except IntegrityError:
        """Handle integrity errors, such as
        when adding an resource that already exists
        """

        db.session.rollback()
        return {"error": "An error occurred. Please review your output and "
                "try again."}, 400


def delete_resource(resource, **kwargs):
    """
    Delete a resource permanently from the database.
    Arguments:
        kwargs["resource"]: The resource to be deleted.
        kwargs["resource_type"]: The type of resource, e.g student, teacher.
    """

    db.session.delete(resource)
    db.session.commit()
    return {"message": "You have successfully deleted the " +
            kwargs["resource_type"] + " with the following ID: " +
            kwargs["id"]}


auth = HTTPBasicAuth()


@auth.error_handler
def error_message(error=None):
    """Returns an error message.
    """

    if not error:
        error = "You are not authorized to access this resource."
    return jsonify({
        "error": error
    }), 403


@app.before_request
def before_request():
    """Validates token. Is run before all API requests apart from
    user registration, login and index.
    """

    if request.endpoint in ["studentlistapi", "studentapi", "teacherlistapi",
                            "teacherapi", "subjectlistapi", "subjectapi"]:
        token = request.headers.get("Authorization")
        if token is not None:
            token_decode_response = User.decode_auth_token(token)
            try:
                user = User.query.get(token_decode_response)
                g.user = user
            except:
                return error_message(token_decode_response), 401
        else:
            return error_message("Please enter a token."), 401


class Index(Resource):
    """Manage responses to the index route.
    URL: /api/v1
    Request method: GET
    """

    def get(self):
        """Return a welcome message
        """

        return {"message": "Welcome to the School API."}
