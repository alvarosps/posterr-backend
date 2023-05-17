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

## Critique

The current back-end application for Posterr is functional for a small scale operation. However, there are several improvements that could be made and scalability issues to consider if the application were to grow significantly.
### Improvement and Refactoring
#### Error Handling

There is some error handling in place, for instance, when a user or post is not found or when rate limits are exceeded. However, the application would benefit from a more thorough and consistent approach to error handling. Errors could be handled in a more centralized manner, using middleware, and more detailed error messages could be provided to assist with debugging.
#### Testing

The application currently lacks automated tests. For the reliability of the application, it is important to have tests that cover all the application's functionalities. Unit tests for the models and routes, integration tests for the endpoints, and stress tests for the performance of the application should be implemented.

#### Logging

The application could also benefit from a logging system. Logging can be used for monitoring, troubleshooting, and auditing purposes. It can help track user activities, system events, and errors that can be useful in debugging and improving the application's performance.
### Scalability
#### Database Optimization

Currently, we are using SQLAlchemy ORM for database interactions which is very convenient and provides us with a lot of useful features out of the box. However, it also adds a level of abstraction that might lead to inefficient queries. As the number of users and posts increases, we need to ensure that our database interactions are optimized.

We could make use of database indexing to speed up the queries, especially for fields that are frequently searched or sorted. Furthermore, database denormalization could be considered for read-heavy workloads to minimize expensive joins.
#### Rate Limiting

While the application has a basic rate limiting in place (limiting the number of posts a user can make in a day), we might want to introduce more sophisticated rate limiting to prevent spamming and abuse of the service. For example, limiting the number of requests per minute or second from a single IP address.
#### Caching

As the number of users and posts grows, caching could be used to reduce database load and speed up request handling. Frequently accessed data like the posts feed could be cached, and cache invalidation strategies would need to be considered.

#### Infrastructure and Deployment

In a real-life situation, we might consider deploying the application on a cloud platform like AWS, Google Cloud, or Azure. Depending on the load, we might need to use multiple servers and load balancing to distribute the network traffic.
### Conclusion

While the current implementation of the Posterr back-end application is functional for small-scale use, there are many areas for improvement and scalability concerns that would need to be addressed for larger-scale operation. By improving error handling and testing, optimizing database interactions, implementing caching, and considering cloud deployment and load balancing, the application could be made more robust and scalable.