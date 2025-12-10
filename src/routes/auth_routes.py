from flask import Blueprint, request
from src.controllers.auth_controller import register, login

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.post("/register")
def register_user():
    return register(request.json)

@auth_routes.post("/login")
def login_user():
    return login(request.json)
