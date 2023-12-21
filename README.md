Task 2 : Flask Task: Library Management System Requirements:
1. Database Setup:
- Use a SQL database (MySQL/ PostgreSQL).
- Create a `Book` table with fields: `id` (primary key), `title`, `author`, `isbn`, and `published_year`.
2. Flask Application:
- Set up a Flask project with the necessary configurations to connect to the database.
- Use SQLAlchemy as the ORM (Object Relational Mapper).
3. API Endpoints:
- `POST /books`: Add a new book to the database.
- `GET /books`: Retrieve a list of all books in the database.
- `GET /books/<id>`: Retrieve details of a specific book by ID.
- `PUT /books/<id>`: Update the details of a specific book.
- `DELETE /books/<id>`: Delete a book from the database.

4. Data Validation:
- Ensure all fields are required for adding a new book.

5. Error Handling:
- Implement proper error handling for database errors and invalid requests.
6. Testing:
- Write unit tests for each endpoint ensuring that all functionalities work as expected.
Steps to Complete:
1. Set up the Flask application and configure the database.
2. Create the `Book` model with SQLAlchemy.
3. Implement the API endpoints, ensuring they interact with the database correctly.
4. Validate incoming data in POST and PUT requests.
5. Implement error handling for common scenarios.
6. Write tests for each API endpoint.
Assessment Criteria:
- Functionality: All endpoints must work as specified.
- Code Quality: Code should be clean, well-organized, and properly commented.
- Error Handling: The application should gracefully handle and report errors.

Submission:
1) Create two separate github repositories for submitting two of the tasks.
2) Include a readme file for necessary setup configurations.
3) Include a demonstration video for submitting the task.
