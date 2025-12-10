from flask import Blueprint, request
from src.controllers.library_controller import *
import jwt
from src.config import Config

library_routes = Blueprint("library_routes", __name__)

def get_user_from_token():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return data["user_id"], data["role"] == "admin"
    except:
        return None, None

# Livros
@library_routes.post("/books")
def create():
    _, is_admin = get_user_from_token()
    if not is_admin:
        return {"error": "Acesso negado"}, 403
    return create_book(request.json)

@library_routes.get("/books")
def read_books():
    return get_books()

@library_routes.put("/books/<int:book_id>")
def update(book_id):
    _, is_admin = get_user_from_token()
    if not is_admin:
        return {"error": "Acesso negado"}, 403
    return update_book(book_id, request.json)

@library_routes.delete("/books/<int:book_id>")
def delete(book_id):
    _, is_admin = get_user_from_token()
    if not is_admin:
        return {"error": "Acesso negado"}, 403
    return delete_book(book_id)

# Reservas
@library_routes.post("/reserve/<int:book_id>")
def reserve(book_id):
    user_id, _ = get_user_from_token()
    if not user_id:
        return {"error": "Token inválido"}, 401
    return reserve_book(user_id, book_id)

@library_routes.get("/reservations")
def read_reservations():
    user_id, is_admin = get_user_from_token()
    return get_reservations(user_id, is_admin)
