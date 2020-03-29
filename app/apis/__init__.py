from app.apis.goodreads import get_isbn_data
from flask import Blueprint


api = Blueprint('api', __name__)

from app.apis import views



