# JobTrack — Job Application Management REST API

JobTrack is a backend REST API for managing job applications, interviews, application statuses, and job-search statistics.

The project is built with **Python, FastAPI, MySQL, SQLAlchemy, JWT authentication, Alembic, and Pytest**.

## Features

* User registration and login
* JWT-based authentication
* Protected API endpoints
* Secure password hashing with bcrypt
* User-specific job data isolation
* Job application CRUD operations
* Job status management
* Job filtering and searching
* Date-range filtering
* Sorting and pagination
* Interview management
* Interview ownership validation
* Application dashboard statistics
* MySQL database integration
* Alembic database migrations
* Automated API tests with Pytest
* Interactive Swagger/OpenAPI documentation
* Health-check and API information endpoints

## Tech Stack

| Technology    | Purpose                      |
| ------------- | ---------------------------- |
| Python        | Backend programming          |
| FastAPI       | REST API framework           |
| MySQL         | Relational database          |
| SQLAlchemy    | ORM and database interaction |
| Pydantic      | Request/response validation  |
| JWT           | Authentication               |
| bcrypt        | Password hashing             |
| Alembic       | Database migrations          |
| Pytest        | Automated testing            |
| Uvicorn       | ASGI server                  |
| python-dotenv | Environment configuration    |

## Project Architecture

```text
Client
  │
  ▼
FastAPI
  │
  ├── Authentication Router
  │      ├── Register
  │      ├── Login
  │      └── Current User
  │
  ├── Jobs Router
  │      ├── CRUD
  │      ├── Filtering
  │      ├── Sorting
  │      ├── Pagination
  │      └── Status Management
  │
  ├── Interviews Router
  │      ├── Create
  │      ├── List
  │      ├── Update
  │      └── Delete
  │
  └── Dashboard Router
         └── Application Statistics
                │
                ▼
          SQLAlchemy ORM
                │
                ▼
              MySQL
```

## Project Structure

```text
jobtrack/
│
├── docs/
|   └── jobtrack-architecture.png
|
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── jobs.py
│   │   ├── interviews.py
│   │   └── dashboard.py
│   │
│   └── alembic/
│       ├── versions/
│       │   ├── 317023b32db4_initial_migration.py
│       │   ├── c284a415be7e_add_company_website.py
│       │   └── 4e5d7093e7c0_add_interviews_table.py
│       │
│       ├── env.py
│       ├── README
│       └── script.py.mako
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_jobs.py
│   ├── test_interviews.py
│   └── test_dashboard.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

## API Endpoints

### Authentication

| Method | Endpoint         | Description                          |
| ------ | ---------------- | ------------------------------------ |
| POST   | `/auth/register` | Register a new user                  |
| POST   | `/auth/login`    | Login and receive JWT token          |
| GET    | `/auth/me`       | Get authenticated user's information |

### Jobs

| Method | Endpoint                | Description              |
| ------ | ----------------------- | ------------------------ |
| POST   | `/jobs`                 | Create a job application |
| GET    | `/jobs`                 | List user's jobs         |
| GET    | `/jobs/{job_id}`        | Get a specific job       |
| PUT    | `/jobs/{job_id}`        | Update a job             |
| PATCH  | `/jobs/{job_id}/status` | Update job status        |
| DELETE | `/jobs/{job_id}`        | Delete a job             |

#### Job List Features

`GET /jobs` supports:

* `status`
* `company`
* `search`
* `from_date`
* `to_date`
* `sort_by`
* `sort_order`
* `skip`
* `limit`

Example:

```text
GET /jobs?status=Interview&sort_by=application_date&sort_order=desc
```

Pagination example:

```text
GET /jobs?skip=0&limit=10
```

### Interviews

| Method | Endpoint                     | Description               |
| ------ | ---------------------------- | ------------------------- |
| POST   | `/jobs/{job_id}/interviews`  | Create an interview       |
| GET    | `/jobs/{job_id}/interviews`  | List interviews for a job |
| PUT    | `/interviews/{interview_id}` | Update an interview       |
| DELETE | `/interviews/{interview_id}` | Delete an interview       |

Interviews are associated with jobs, and access is validated through the owner of the associated job.

### Dashboard

| Method | Endpoint           | Description                |
| ------ | ------------------ | -------------------------- |
| GET    | `/dashboard/stats` | Get application statistics |

The dashboard returns:

* Total jobs
* Applied
* Shortlisted
* Assessment
* Interview
* Selected
* Rejected
* Withdrawn
* Total interviews

### General Endpoints

| Method | Endpoint  | Description         |
| ------ | --------- | ------------------- |
| GET    | `/`       | API welcome message |
| GET    | `/health` | API health status   |
| GET    | `/about`  | API information     |

## Authentication

JobTrack uses **JWT Bearer authentication**.

The authentication flow is:

```text
Register
   │
   ▼
Password hashed with bcrypt
   │
   ▼
User stored in MySQL
   │
   ▼
Login
   │
   ▼
JWT access token
   │
   ▼
Authorization: Bearer <token>
   │
   ▼
Protected endpoint
```

Protected resources verify the authenticated user's ID before accessing jobs or interviews.

This prevents one user from accessing, updating, or deleting another user's data.

## Job Statuses

Job applications can use the following statuses:

```text
Applied
Shortlisted
Assessment
Interview
Selected
Rejected
Withdrawn
```

## Database

The project uses **MySQL** with **SQLAlchemy**.

Main entities:

```text
User
 │
 └── Jobs
      │
      └── Interviews
```

Relationships:

* One User → Many Jobs
* One Job → Many Interviews

## Database Migrations

Alembic is used to manage database schema changes.

Create a migration:

```bash
alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
alembic upgrade head
```

Check migration status:

```bash
alembic current
```

## Testing

JobTrack uses **Pytest** for automated API testing.

The test suite covers:

* User registration
* Login
* JWT authentication
* Invalid authentication
* Protected endpoints
* Duplicate username validation
* Duplicate email validation
* Job CRUD
* Job filtering
* Pagination
* Job status updates
* Nonexistent resources
* User ownership/security
* Interview CRUD
* Interview ownership
* Dashboard statistics

Current test status:

```text
23 tests passed
0 tests failed
```

Run all tests:

```bash
pytest -v
```

## Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd jobtrack
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Create the database:

```sql
CREATE DATABASE jobtrack;
```

Create a test database:

```sql
CREATE DATABASE jobtrack_test;
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/jobtrack
TEST_DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/jobtrack_test

SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit `.env` to GitHub.

### 6. Run database migrations

```bash
alembic upgrade head
```

### 7. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

You can use Swagger UI to:

1. Register a user
2. Login
3. Copy the JWT token
4. Authorize using the Bearer token
5. Test protected endpoints

## Environment Variables

| Variable                      | Description                           |
| ----------------------------- | ------------------------------------- |
| `DATABASE_URL`                | Development MySQL database connection |
| `TEST_DATABASE_URL`           | Test MySQL database connection        |
| `SECRET_KEY`                  | JWT signing secret                    |
| `ALGORITHM`                   | JWT algorithm                         |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiration time                   |

## Security

The project implements:

* JWT authentication
* Password hashing with bcrypt
* Protected API routes
* User ownership validation
* Environment-based secrets
* Separate test database
* Input validation with Pydantic

The `.env` file is excluded from Git using `.gitignore`.

## Error Handling

The API returns appropriate HTTP status codes for common situations.

Examples:

```text
201 Created
400 Bad Request
401 Unauthorized
404 Not Found
```

Examples include:

* Duplicate username → `400`
* Duplicate email → `400`
* Missing/invalid authentication → `401`
* Nonexistent or unauthorized resource → `404`

## Future Improvements

Potential future improvements include:

* Refresh tokens
* Password reset
* Email notifications
* Job application reminders
* Resume/document upload
* Advanced analytics
* Background tasks
* Docker deployment
* CI/CD pipeline
* Cloud deployment
* Role-based authorization
* API rate limiting

## Author

**Dhruv Patel**

B.Tech — Information & Communication Technology

GitHub: `https://github.com/DJPATEL001`

LinkedIn: `https://www.linkedin.com/in/dhruvpatel-ict/`

## License

This project is intended as a portfolio and learning project.
