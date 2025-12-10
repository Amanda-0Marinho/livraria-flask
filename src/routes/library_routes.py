from flask import Blueprint, request
from src.controllers.library_controller import create_book, get_books, update_book, delete_book, reserve_book, get_reservations
from src.controllers.auth_controller import login_required, admin_required

library_routes = Blueprint("library_routes", __name__)

@library_routes.post("/books")
@admin_required
def create(data):
    return create_book(data, request.json)

@library_routes.get("/books")
def read_books():
    return get_books()

@library_routes.put("/books/<int:book_id>")
@admin_required
def update(data, book_id):
    return update_book(data, book_id, request.json)

@library_routes.delete("/books/<int:book_id>")
@admin_required
def delete(data, book_id):
    return delete_book(data, book_id)

@library_routes.post("/reserve/<int:book_id>")
@login_required
def reserve(data, book_id):
    return reserve_book(data, book_id)

@library_routes.get("/reservations")
@login_required
def read_reservations(data):
    return get_reservations(data["user_id"], data["role"] == "admin")
