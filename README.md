# Notes Application Backend with FastAPI

A full-featured, secure backend for a notes app built using FastAPI, MySQL, SQLAlchemy, JWT authentication, and Docker.

***

## Features

- User registration and login with JWT (JSON Web Tokens) for stateless authentication
- Secure password hashing using bcrypt
- CRUD endpoints for user notes, supporting multi-user isolation
- MySQL database managed via Docker containerization
- Alembic migrations for database schema version control
- Fully Dockerized with `docker-compose` for easy deployment

***

## Project Structure

```
main.py
models.py
database.py
schemas.py
auth.py
requirements.txt
Dockerfile
alembic.ini
alembic/
  env.py
  versions/
routers/
  notes.py
  users.py
docker-compose.yml
```

***

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd NotesApplication
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

- On Linux/macOS:

  ```bash
  source .venv/bin/activate
  ```

- On Windows:

  ```bash
  .venv\Scripts\activate
  ```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run MySQL Docker Container for Notes Database

```bash
docker run --name notes-mysql \
  -e MYSQL_DATABASE=notesdb \
  -e MYSQL_USER=notesuser \
  -e MYSQL_PASSWORD=notespwd \
  -e MYSQL_ROOT_PASSWORD=rootpwd \
  -p 3306:3306 \
  -v notes_db_data:/var/lib/mysql \
  -d mysql:8.0
```

### 6. Update Alembic Configuration

Edit `alembic.ini` and update `sqlalchemy.url`:

```
sqlalchemy.url = mysql+mysqlconnector://notesuser:notespwd@localhost:3306/notesdb
```

Ensure it points to your MySQL Docker container.

### 7. Grant Permissions to Alembic Folder (if required)

```bash
sudo chown -R $(whoami) alembic
chmod -R 755 alembic
```

### 8. Update Docker MySQL Connection in `run.sh` and Run It

Ensure `run.sh` has correct MySQL connection credentials matching your Docker container, then run:

```bash
chmod +x run.sh
./run.sh up
```

### 9. Wait for Application to Start Running

Monitor logs to ensure database and FastAPI start without errors.

### 10. Access API Documentation and Test

Open your browser and visit:

```
http://localhost:8000/docs
```

Test user registration, login, and the notes CRUD endpoints using the interactive Swagger UI.

***

## API Endpoints Overview

### User Authentication

- `POST /register`
  Register a new user. Provide username, email, and password. Password is securely hashed.

- `POST /login`
  Login with username and password. Returns a JWT token to be used as Bearer token.

- `GET /me` (Protected)
  Retrieve the currently authenticated user profile using the JWT token.

### Notes Management (Protected - JWT Required)

- `POST /notes/`
  Create a new note linked to the authenticated user.

- `GET /notes/`
  List all notes belonging to the authenticated user.

- `GET /notes/{note_id}`
  Retrieve a single note by ID if it belongs to the user.

- `PUT /notes/{note_id}`
  Update an existing note if it belongs to the user.

- `DELETE /notes/{note_id}`
  Delete a note by ID if it belongs to the user.

***

## Authentication Details

- Use the JWT token returned from `/login` in the `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

- Protected endpoints validate the token for user identity.

***

## Dependencies

- fastapi==0.103.2
- uvicorn==0.23.2
- sqlalchemy==2.0.21
- mysql-connector-python==8.1.0
- alembic==1.12.0
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- python-dotenv==1.0.0
- pydantic[email]==2.11.9
- python-multipart==0.0.29
