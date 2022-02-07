# About this project
This project is a coding test for a Backend Developer position at Nium and was developed and tested on Apple M1 running MacOS Monterey 12.1. Also was tested on a Ubuntu 20.04

# Technologies and libs
- Python 3.10
- PostgreSQL 14
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pytest
- Docker

# TODOs
- Implement Account transactions, such as deposit, withdraw and transfer
- Implement simple Blockchain
- Implement Redis for caching
- Implement Celery for queuing
# Running the app
1. Clone project to a directory of your preference
2. On the directory that the project was cloned run `docker-compose up`
3. Run `docker-compose exec web alembic upgrade head` to run migrations
4. App should be available at `http://localhost:8000`
5. PgAdmin should be available at `http://localhost:5050`

# API Documentation (swagger)
1. Go to `http://localhost:8000/docs` for API documentation

# Running tests
1. Run `docker-compose exec web pytest app/tests`