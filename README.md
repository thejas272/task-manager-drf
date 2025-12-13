# Task Manager REST API

A Django REST Framework based Task Manager API with JWT authentication and role-based access control.

## Features
- User Registration & Login
- JWT Authentication (Access & Refresh tokens)
- Task CRUD operations
- Role-Based Access Control
- Secure ownership enforcement

## Roles
- **Admin (is_staff=True)**
  - Can create, view, update, and delete any user's tasks
- **Normal User**
  - Can manage only their own tasks

## Authentication
This API uses JWT authentication via `djangorestframework-simplejwt`.

- Access Token lifetime: 60 minutes
- Refresh Token lifetime: 1 day

## API Endpoints

### Auth
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`

### Tasks
- `POST /api/tasks/create/`
- `GET /api/tasks/list/`
- `GET /api/tasks/retrieve/<id>/`
- `PUT /api/tasks/update/<id>/`
- `DELETE /api/tasks/delete/<id>/`





## API Usage Examples

### Register User
- `POST /api/auth/register/`

```json
{
    "username": "thejas272",
    "password": "A strong password",
    "email":"A valid email"
}



{
    "username": "thejas272",
    "email": "Email id passed in request body"
}




### Obtain JWT Tokens(login and refresh)

- `POST /api/auth/login/`

```json
{
    "username": "thejas272",
    "password": "A strong password"
}


{
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}


- `POST /api/auth/refresh/`

```json
{
    "refresh": "<refresh_token>"
}

{
    "access": "<access_token>"
}



### Using JWT in Requests

Authorization: Bearer <access_token>


### Creaing A Task

```json
{
  "title": "Finish assignment",
  "description": "Complete Django Task Manager API",
  "status": false
}

Normal users → owner is set automatically

Admin users → can optionally provide owner





## Setup Instructions

### 1. Clone repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows


### 3. Install Dependencies
```bash
pip install -r requirements.txt


### 4. Environment Varibales
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost


### 5. Run Migrations
```bash
python manage.py migrate


### 5. Create Admin Superuser
```bash
python manage.py createsuperuser


### 6. Run server
```bash
python manage.py runserver