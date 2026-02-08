# WorkSite - Construction Workforce Job Portal Backend

A Django REST Framework backend for the WorkSite construction workforce job portal, featuring role-based access control, Google OAuth integration, and atomic job vacancy management.

## Features

- **Three User Roles**: Worker, Employer, and Admin
- **Dual Authentication**: Standard email/password and Google OAuth 2.0
- **Job Management**: Create, list, and delete job postings
- **Application System**: One-click job applications with atomic slot filling
- **Auto-closure**: Jobs automatically close when all positions are filled
- **Race Condition Prevention**: Atomic operations using Django F() expressions
- **Location Filtering**: Filter jobs by city
- **Admin Panel**: Full admin interface for user and job management
- **API Documentation**: Swagger UI at `/api/docs/`

## Tech Stack

- **Framework**: Django 5.0+ with Django REST Framework
- **Database**: PostgreSQL (configurable to SQLite for development)
- **Authentication**: Session-based with Google OAuth support
- **API Documentation**: drf-spectacular (Swagger/OpenAPI)

## Installation

### 1. Clone the repository

```bash
cd worksite
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# For development, SQLite is used by default
DEBUG=True
SECRET_KEY=your-secret-key-here

# For Google OAuth (optional)
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret

# For PostgreSQL (optional)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=worksite_db
DB_USER=postgres
DB_PASSWORD=your-password
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create superuser

```bash
python manage.py createsuperuser
```

### 7. Run development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login user | No |
| POST | `/api/auth/logout` | Logout user | Yes |
| GET | `/api/auth/status` | Check auth status | Yes |
| GET | `/api/auth/google` | Initiate Google OAuth | No |
| GET | `/api/auth/google/callback` | OAuth callback | No |
| POST | `/api/auth/google/complete` | Complete OAuth profile | Yes |

### User Management (Admin Only)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/users/` | List all users | Admin |
| DELETE | `/api/users/{id}/` | Delete user | Admin |

### Jobs

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/jobs/` | List jobs | Yes |
| POST | `/api/jobs/` | Create job | Employer |
| DELETE | `/api/jobs/{id}/` | Delete job | Employer/Admin |
| POST | `/api/jobs/{id}/apply/` | Apply for job | Worker |
| GET | `/api/jobs/{id}/applications/` | List job applications | Employer/Admin |

### Applications

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/applications/my` | Get my applications | Worker |
| PUT | `/api/applications/status` | Update application status | Employer |
| DELETE | `/api/jobs/{job_id}/applications/{worker_id}` | Remove worker | Employer |

## Query Parameters

### List Jobs (`GET /api/jobs/`)

- `status`: Filter by job status (`open` or `closed`)
- `city`: Filter by employer city
- `my_jobs`: Set to `true` to see only your posted jobs (employers only)

## Request/Response Examples

### Register User

```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "worker@example.com",
  "password": "securepass123",
  "password2": "securepass123",
  "full_name": "John Doe",
  "role": "worker",
  "city": "Mumbai"
}
```

### Create Job

```bash
POST /api/jobs/
Content-Type: application/json
Authorization: Session

{
  "title": "Construction Worker Needed",
  "description": "Looking for experienced workers",
  "daily_wage": 800.00,
  "required_workers": 5
}
```

### Apply for Job

```bash
POST /api/jobs/1/apply/
Authorization: Session
```

### Accept Application

```bash
PUT /api/applications/status
Content-Type: application/json
Authorization: Session

{
  "application_id": 1,
  "status": "accepted"
}
```

## Database Models

### User
- email (unique)
- full_name
- role (worker/employer/admin)
- city
- google_id (for OAuth)
- oauth_provider
- is_oauth_complete
- profile_photo

### Job
- employer (FK to User)
- title
- description
- daily_wage
- required_workers
- filled_slots (auto-incremented)
- status (open/closed - auto-managed)

### Application
- job (FK to Job)
- worker (FK to User)
- status (pending/accepted/rejected)
- Unique constraint on (job, worker)

## Atomic Operations

The backend uses Django's `F()` expressions and `select_for_update()` to ensure atomic operations:

- **Job Application**: Prevents race conditions when multiple workers apply simultaneously
- **Slot Filling**: Atomically increments `filled_slots` when applications are accepted
- **Auto-closure**: Automatically closes jobs when `filled_slots == required_workers`

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:8000/api/auth/google/callback`
6. Copy Client ID and Secret to `.env` file

## Admin Panel

Access the Django admin at `http://localhost:8000/admin/` with superuser credentials.

Features:
- User management
- Job management
- Application management
- Role assignment

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

## Development

### Run Tests

```bash
python manage.py test
```

### Create Migrations

```bash
python manage.py makemigrations
```

### Apply Migrations

```bash
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Configure PostgreSQL database
3. Set secure `SECRET_KEY`
4. Configure `ALLOWED_HOSTS`
5. Set up HTTPS
6. Collect static files: `python manage.py collectstatic`
7. Use production-grade WSGI server (gunicorn, uwsgi)

## License

MIT License

## Contributors

- Tejas Patare
- Isha Vaidya
- Kartavya Gore
