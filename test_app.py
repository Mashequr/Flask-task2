import unittest
from flask import Flask
from flask_restful import Api, marshal_with, fields
from flask_testing import TestCase
from app import BooksResource, BookResource, db, app

book_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.String,
    'isbn': fields.String,
    'published_year': fields.Integer,
}

class TestApp(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        # Initialize the database with the app context
        with app.app_context():
            db.init_app(app)
            db.create_all()

        api = Api(app)
        api.add_resource(BooksResource, '/')
        api.add_resource(BookResource, '/', '/<int:book_id>')

        return app

    def setUp(self):
        # Add any setup logic here
        pass

    def tearDown(self):
        # Add any teardown logic here
        pass
    
    @marshal_with(book_fields)
    def test_get_all_books(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    @marshal_with(book_fields)
    def test_add_book(self):
        data = {'title': 'Test Book', 'author': 'Test Author', 'isbn': '1234567890', 'published_year': 2022}
        response = self.client.post('/', json=data)
        self.assertEqual(response.status_code, 201)  # Changed from 200 to 201

    @marshal_with(book_fields)
    def test_get_single_book(self):
        data = {'title': 'kadfhdshf', 'author': 'KAwrfef', 'isbn': '978124341890', 'published_year': 2001}
        create_response = self.client.post('/', json=data)
        self.assertEqual(create_response.status_code, 201)

        # Retrieve the book ID from the created book
        created_book_id = create_response.json['id']

        # Now, test getting the book by ID
        response = self.client.get(f'/{created_book_id}')
        self.assertEqual(response.status_code, 200)

        # Check attributes of the returned book
        book = response.json
        self.assertEqual(book['id'], created_book_id)
        self.assertEqual(book['title'], 'kadfhdshf')
        self.assertEqual(book['author'], 'KAwrfef')
        self.assertEqual(book['isbn'], '978124341890')
        self.assertEqual(book['published_year'], 2001)

    @marshal_with(book_fields)
    def test_update_book(self):
        data = {'title': 'kadfhdshf', 'author': 'KAwrfef', 'isbn': '978124341890', 'published_year': 2001}
        create_response = self.client.post('/', json=data)
        self.assertEqual(create_response.status_code, 201)

        # Retrieve the book ID from the created book
        created_book_id = create_response.json['id']

        # Now, test updating the book
        update_data = {'title': 'Updated Title'}
        update_response = self.client.put(f'/{created_book_id}', json=update_data)
        self.assertEqual(update_response.status_code, 200)

        # Optionally, you can check the updated book's attributes
        updated_response = self.client.get(f'/{created_book_id}')
        updated_book = updated_response.json
        self.assertEqual(updated_book['title'], 'Updated Title')

    @marshal_with(book_fields)
    def test_delete_book(self):
        # Create a book first
        data = {'title': 'kadfhdshf', 'author': 'KAwrfef', 'isbn': '978124341890', 'published_year': 2001}
        create_response = self.client.post('/', json=data)
        self.assertEqual(create_response.status_code, 201)

        # Retrieve the book ID from the created book
        created_book_id = create_response.json['id']

        # Now, test deleting the book
        delete_response = self.client.delete(f'/{created_book_id}')
        self.assertEqual(delete_response.status_code, 204)

        # Attempt to get the deleted book
        get_response = self.client.get(f'/{created_book_id}')
        
        # Print the response content
        print(get_response.get_json())

        # Check if the ID is 0 (indicating a successful delete)
        self.assertEqual(get_response.json['id'], 0)

if __name__ == '__main__':
    unittest.main()
