from flask_restful import marshal
from sqlalchemy.exc import IntegrityError

from app import db
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
        if kwargs["create"]:
            if kwargs["resource_type"] == "user":
                # Get user's auth token
                user = User.query.filter_by(
                    username=kwargs["username"]).first()
                auth_token = user.generate_auth_token(user.id)

                response = {"message": "You have successfully signed up.",
                            "token": auth_token.decode()}
            else:
                response = marshal(kwargs["resource"], kwargs["serializer"])
                message = {"message": "You have successfully created a new " +
                           kwargs["resource_type"] + "."}
                response.update(message)
            return response, 201
        else:
            response = marshal(kwargs["resource"], kwargs["serializer"])
            message = {"message": "You have successfully edited the " +
                       kwargs["resource_type"] + "."}
            response.update(message)
            return response

    except IntegrityError as e:
        """Handle integrity errors, such as
        when adding an resource that already exists
        """

        db.session.rollback()
        return {"error": str(e)}, 400


def delete_resource(resource, **kwargs):
    """
    Delete a resource permanently from the database.
    Arguments:
        kwargs["resource"]: The resource to be deleted.
        kwargs["resource_type"]: The type of resource, i.e user, hospital, etc.
    """

    db.session.delete(resource)
    db.session.commit()
    return {"message": "You have successfully deleted the " +
            kwargs["resource_type"] + " with the following ID: " +
            kwargs["id"] + "."}
