from app import api, app
from app.resources import Index
from app.resources.auth import UserLogin, UserRegister


""" Defining the API endpoints """
api.add_resource(Index, "/")
api.add_resource(UserRegister, "/auth/register")
api.add_resource(UserLogin, "/auth/login")

if __name__ == '__main__':
    app.run()
