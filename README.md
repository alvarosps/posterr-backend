# Posterr Backend

Posterr is a backend application for a simple social media platform where users can create and repost content. This application is built using Python, Flask, and SQLAlchemy, and uses PostgreSQL as the database.

## Setup and Run Instructions

### Without Docker
1. Install Python 3.8 or higher and create a virtual environment:
`python3 -m venv venv`

2. Activate the virtual environment:
- On macOS and Linux:
`source venv/bin/activate`
- On Windows:
`venv\Scripts\activate`

3. Install the required packages:
`pip install -r requirements.txt`

4. Create a PostgreSQL database and user with the necessary privileges using the 'init.sql' script.

5. Run the migrations:
`flask db upgrade`

6. Start the application:
`flask run`

The application will be running at http://localhost:5000

### With Docker
1. Install Docker and Docker Compose.

2. Build the Docker image and run the containers:
`docker-compose up -d`

The application will be runnin at http://localhost:5000

# Important: When using the frontend application without user management
If you are using the frontend application that does not support used for the moment, start the backend, and add a user to it, so we have user_id = 1 in the database.
For that, do a POST call to http://localhost:5000/api/users with a JSON body:
```
{
    "username": "an username you want to put"
}
```
## Usage

You can now interact with the Posterr backend API. The available endpoints are:

- GET /api/users: Get all users
- POST /api/users: Create a new user
- GET /api/posts: Get all posts
- POST /api/posts: Create a new post

To create and fetch users and posts, you can use a REST client like Postman or Insomnia.

## Cleanup

To stop and remove the Docker containers, use the following command:
`docker-compose down`

This will also remove the PostgreSQL data volume. If you want to keep the colume, you can use:
`docker-compose down --volumes`