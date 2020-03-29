import requests
import os


GOODREADS_KEY = os.getenv("GOODREADSKEY")


def get_isbn_data(isbn):
    r = requests.get("https://www.goodreads.com/book/review_counts.json",
                 params={"key":GOODREADS_KEY, "isbns":isbn})
    return r


if __name__ == "__main__":
    isbn = "0380795272"
    r = get_isbn_data(isbn)
    print(dict(r.json()))

