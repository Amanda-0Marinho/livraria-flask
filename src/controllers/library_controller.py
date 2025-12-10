from flask import jsonify
from src.extensions import db
from src.models.book import Book
from src.models.reservation import Reservation

def create_book(data):
    book = Book(
        title=data.get("title"),
        author=data.get("author"),
        genre=data.get("genre"),
        status="available"
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({"message": "Livro criado"}), 201

def get_books():
    books = Book.query.all()
    return jsonify([{
        "id": b.id,
        "title": b.title,
        "author": b.author,
        "genre": b.genre,
        "status": b.status
    } for b in books])

def update_book(book_id, data):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Livro não encontrado"}), 404

    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    book.genre = data.get("genre", book.genre)
    book.status = data.get("status", book.status)

    db.session.commit()
    return jsonify({"message": "Livro atualizado"})

def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Livro não encontrado"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Livro deletado"})

def reserve_book(user_id, book_id):
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

    return jsonify([{
        "id": r.id,
        "user_id": r.user_id,
        "book_id": r.book_id,
        "reserved_at": r.reserved_at
    } for r in reservations])
