## PostAPP

PostAPP is a RESTful API built using **FastAPI** and **PostgreSQL** to manage posts efficiently. It provides CRUD operations and follows RESTful principles, ensuring high performance and seamless integration.

## Features
- FastAPI-based backend for high-speed API requests
- PostgreSQL for reliable and scalable data storage
- CRUD operations for managing posts
- JSON-based responses for easy frontend integration
- Asynchronous request handling for better performance

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.8+
- PostgreSQL
- pip

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Sumit0ubey/PostAPP.git
   cd PostAPP
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables for PostgreSQL connection:
   ```bash
   export DATABASE_URL="postgresql://username:password@localhost/dbname"
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

| Method | Endpoint       | Description          |
|--------|---------------|----------------------|
| GET    | `/`           | Retrieve APP info   |
| GET    | `/posts`      | Retrieve all posts  |
| GET    | `/posts/{id}` | Get a specific post |
| POST   | `/posts`      | Create a new post   |
| PUT    | `/posts/{id}` | Update a post       |
| DELETE | `/posts/{id}` | Delete a post       |
| PUT    | `/likes`      |Like a specific posts|
| POST   | `/users`      | Create a new user   |
| GET    | `/users/`     | Get all user        |
| GET    | `/users/{id}` | Get a user          |
| POST   | `/auth/login` | login as a user     |
| GET    | `/auth/logout`| logout a user       |

## Running Tests
To run tests, use:
```bash
pytest
```

## License
This project is licensed under the MIT License.

## Author
Developed by [Sumit dubey](https://github.com/Sumit0ubey).

