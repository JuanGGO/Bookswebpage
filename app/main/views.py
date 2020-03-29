from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import main
from app.models import Book, User, Review
from app import db
from app.apis import get_isbn_data


@main.route("/")
def index():
    return render_template("auth/login.html")


@main.route("/user/<string:username>")
@login_required
def user(username):
    user_ = User.query.filter_by(username=username).first()
    if user_:
        if current_user.id == user_.id:
            return render_template("main/user.html", user=user_)
        else:
            return render_template("error.html", message="User is not logged-in please log-in")
    else:
        return render_template("error.html", message="User does not exists!")


@main.route("/search", methods=['POST'])
@login_required
def search():
    isbn_code = request.form.get("bookisbn")
    if isbn_code:
        book = Book.query.filter_by(isbn=isbn_code).first()
        if book:
            return redirect(url_for('main.bookpage', isbn=book.isbn))
    return render_template("main/user.html", username=current_user)


@main.route("/book/<string:isbn>")
@login_required
def bookpage(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    if book is None:
        return render_template("error.html", message="Book does not exists")

    goodreads_info = get_isbn_data(isbn)
    reviews = Review.query.all()
    return render_template("main/book.html", book=book, reviews=reviews, goodreads_info=goodreads_info)


@main.route("/allbooks")
def allbooks():
    books = Book.query.order_by(Book.title.asc()).all()
    return render_template("main/allbooks.html", books=books)


@main.route("/addreview/<string:isbn>", methods=['POST'])
@login_required
def add_review(isbn):
    comment = request.form.get("comment")
    if comment.isspace():
        return render_template("error.html", message="You should write a string")

    # Adding the review
    book = Book.query.filter_by(isbn=isbn).first()
    if book is None:
        return render_template("error.html", message="The book isbn does not exist!")

    user_id = current_user.id
    book_id = book.id
    username = current_user.username
    book_title = book.title
    book_isbn = book.isbn

    review = Review(user_id=user_id, book_id=book_id, username=username,
                    book_title=book_title, book_isbn=book_isbn, review=comment)

    db.session.add(review)
    db.session.commit()
    reviews = Review.query.all()
    goodreads_info = get_isbn_data(book_isbn)
    return render_template("main/book.html", reviews=reviews, book=book, goodreads_info=goodreads_info)


@main.route("/remove_review/<int:review_id>")
def remove_review(review_id):
    review = Review.query.filter_by(id=review_id).first()
    book = Book.query.filter_by(isbn=review.book_isbn)
    if review:
        Review.query.filter_by(id=review_id).delete()
        db.session.commit()
    goodreads_info = get_isbn_data(book.isbn)
    reviews = Review.query.all()
    return render_template("main/book.html", reviews=reviews, book=book, goodreads_info=goodreads_info)


@main.route("/userprofile/<string:username>")
def profile(username):
    user_ = User.query.filter_by(username=username).first()
    if user_:
        return render_template("main/profile.html", userprofile=user_)

    return render_template("error.html", message="User does not exist")





