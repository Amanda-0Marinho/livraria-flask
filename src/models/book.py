from src.extensions import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    status = db.Column(db.String(20), default="available")

    reservations = db.relationship("Reservation", backref="book", lazy=True)
