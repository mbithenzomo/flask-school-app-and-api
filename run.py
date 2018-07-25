from app import api, app
from app.resources import Index
from app.resources.auth import UserLogin, UserRegister
from app.resources.students import StudentListAPI, StudentAPI
from app.resources.teachers import TeacherListAPI, TeacherAPI
from app.resources.subjects import SubjectListAPI, SubjectAPI


""" Defining the API endpoints """
api.add_resource(Index, "")
api.add_resource(UserRegister, "/auth/register")
api.add_resource(UserLogin, "/auth/login")
api.add_resource(StudentListAPI, "/students")
api.add_resource(StudentAPI, "/students/<string:id>")
api.add_resource(TeacherListAPI, "/teachers")
api.add_resource(TeacherAPI, "/teachers/<string:id>")
api.add_resource(SubjectListAPI, "/subjects")
api.add_resource(SubjectAPI, "/subjects/<string:id>")

if __name__ == '__main__':
    app.run()
