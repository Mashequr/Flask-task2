from flask import Flask, request, jsonify
from flask_restful import Resource, Api, marshal_with, fields, abort, reqparse
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, DataError

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass1234@localhost:5432/library_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    isbn = db.Column(db.String, nullable=False)
    published_year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

fakeDatabase = {
    1:{'name':'Clean car'},
    2:{'name':'Write blog'},
    3:{'name':'Start stream'},
}

# API endpoints
book_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.String,
    'isbn': fields.String,
    'published_year': fields.Integer,
}

class BooksResource(Resource):
    @marshal_with(book_fields)
    def get(self):
        books = Book.query.all()
        return books

    @marshal_with(book_fields)
    def post(self):
        try:
            data = request.json
            book = Book(**data)
            db.session.add(book)
            db.session.commit()
            return book, 201  # Returning 201 Created status code
        except IntegrityError:
            return {'error': 'Integrity violation: Check your input data.'}, 400
        except DataError:
            return {'error': 'Invalid data format.'}, 400
        except Exception as e:
            return {'error': str(e)}, 500

class BookResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, help='Title of the book')
    parser.add_argument('author', type=str, help='Author of the book')
    parser.add_argument('isbn', type=str, help='ISBN of the book')
    parser.add_argument('published_year', type=int, help='Published year of the book')

    @marshal_with(book_fields)
    def get(self, book_id):
        try:
            book = Book.query.get_or_404(book_id)
            return book
        except Exception as e:
            return {'error': str(e)}, 500

    @marshal_with(book_fields)
    def put(self, book_id):
        try:
            book = Book.query.get_or_404(book_id)
            data = request.json
            for key, value in data.items():
                setattr(book, key, value)
            db.session.commit()
            return book
        except IntegrityError:
            return {'error': 'Integrity violation: Check your input data.'}, 400
        except DataError:
            return {'error': 'Invalid data format.'}, 400
        except Exception as e:
            return {'error': str(e)}, 500

    @marshal_with(book_fields)
    def delete(self, book_id):
        try:
            book = Book.query.get_or_404(book_id)
            db.session.delete(book)
            db.session.commit()
            return '', 204  # Returning 204 No Content status code
        except HTTPException as e:
            return {'error': str(e)}, e.code
        except Exception as e:
            return {'error': str(e)}, 500
    
# API resources
    
api.add_resource(BooksResource, '/')
api.add_resource(BookResource,  '/', '/<int:book_id>')

@app.route('/')
def display_books():
    # Query all books from the database
    books = Book.query.all()

    # Convert the list of books to a JSON format
    books_json = [{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn,
        'published_year': book.published_year
    } for book in books]

    # Return the JSON response
    return jsonify(books_json)

if __name__ == '__main__':
    app.testing = True
    app.run(debug=True)