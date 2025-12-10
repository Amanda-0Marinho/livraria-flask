from flask import jsonify
from src.extensions import db
from src.models.book import Book
from src.models.reservation import Reservation
from src.routes.auth_routes import login_required, admin_required


@login_required
def create_book(data, req):
    if not req.get("title"):
        return jsonify({"error": "Título obrigatório"}), 400

    book = Book(
        title=req.get("title"),
        author=req.get("author"),
        genre=req.get("genre"),
        status="available"
    )

    db.session.add(book)
    db.session.commit()

    return jsonify({"message": "Livro criado", "id": book.id}), 201


def get_books():
    books = Book.query.all()
    return jsonify([
        {
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "genre": b.genre,
            "status": b.status
        } for b in books
    ])


@admin_required
def update_book(data, book_id, req):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Livro não encontrado"}), 404

    book.title = req.get("title", book.title)
    book.author = req.get("author", book.author)
    book.genre = req.get("genre", book.genre)
    book.status = req.get("status", book.status)

    db.session.commit()
    return jsonify({"message": "Livro atualizado"})


@admin_required
def delete_book(data, book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Livro não encontrado"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Livro deletado"})


@login_required
def reserve_book(data, book_id):
    user_id = data["user_id"]

    book = Book.query.get(book_id)
    if not book or book.status != "available":
        return jsonify({"error": "Livro indisponível"}), 400

    reservation = Reservation(user_id=user_id, book_id=book_id)
    book.status = "reserved"

    db.session.add(reservation)
    db.session.commit()

    return jsonify({"message": "Livro reservado"}), 201


def get_reservations(user_id=None, is_admin=False):
    if is_admin:
        reservations = Reservation.query.all()
    else:
        reservations = Reservation.query.filter_by(user_id=user_id).all()

    if not reservations:
        return jsonify({"message": "Nenhuma reserva encontrada"}), 200

    return jsonify([
        {
            "id": r.id,
            "user_id": r.user_id,
            "book_id": r.book_id,
            "reserved_at": r.reserved_at
        } for r in reservations
    ])
