from app import api, app
from app.resources import Index
from app.resources.auth import UserLogin, UserRegister
from app.resources.students import StudentListAPI, StudentAPI
from app.resources.teachers import TeacherListAPI, TeacherAPI


""" Defining the API endpoints """
api.add_resource(Index, "/")
api.add_resource(UserRegister, "/auth/register")
api.add_resource(UserLogin, "/auth/login")
api.add_resource(StudentListAPI, "/students")
api.add_resource(StudentAPI, "/students/<string:id>")
api.add_resource(TeacherListAPI, "/teachers")
api.add_resource(TeacherAPI, "/teachers/<string:id>")

if __name__ == '__main__':
    app.run()
