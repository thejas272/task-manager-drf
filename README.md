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

## Setup Instructions

### 1. Clone repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
