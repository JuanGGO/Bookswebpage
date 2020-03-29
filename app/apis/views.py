from . import api
from app.models import Book, Review
from flask import jsonify


@api.route("/api/<string:isbn>")
def send_book_data(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        json_file = {}
        json_file["title"] = book.title
        json_file["author"] = book.author
        json_file["year"] = book.year
        json_file["isbn"] = book.isbn
        json_file["review_count"] = Review.query.filter_by(book_id=book.id).count()

    return jsonify(json_file)

