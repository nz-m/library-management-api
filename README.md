# Library Management System

This is a simple Django-based Library Management System using Django REST Framework. The application allows users to manage library items, users, lending records, return transactions, penalties, and payments. It also integrates JWT authentication via the `djoser` library for secure API access.

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Admin Interface](#admin-interface)

## Setup Instructions

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- Virtualenv (recommended)

### Step 1: Clone the repository

```bash
git clone https://github.com/nz-m/library-management-api.git
cd library-management-api
```


### Step 2: Create and activate a virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run migrations

```bash
python manage.py migrate
```

### Step 5: Create a superuser

```bash
python manage.py createsuperuser
```

### Step 6: Run the development server

```bash
python manage.py runserver
```

The application will be available at `http://:127.0.0.1:8000/`.

# API Endpoints

## User Endpoints

- **List all users**  
  `GET /users/`
  
- **Create a new user**  
  `POST /users/`

- **Retrieve a specific user**  
  `GET /users/{id}/`

- **Update a specific user**  
  `PUT /users/{id}/`

- **Partially update a specific user**  
  `PATCH /users/{id}/`

- **Delete a specific user**  
  `DELETE /users/{id}/`

## Library Item Endpoints

- **List all library items**  
  `GET /library-items/`

- **Create a new library item**  
  `POST /library-items/`

- **Retrieve a specific library item**  
  `GET /library-items/{id}/`

- **Update a specific library item**  
  `PUT /library-items/{id}/`

- **Partially update a specific library item**  
  `PATCH /library-items/{id}/`

- **Delete a specific library item**  
  `DELETE /library-items/{id}/`

## Lending Record Endpoints

- **List all lending records**  
  `GET /lending-records/`

- **Create a new lending record**  
  `POST /lending-records/`

- **Retrieve a specific lending record**  
  `GET /lending-records/{id}/`

- **Update a specific lending record**  
  `PUT /lending-records/{id}/`

- **Partially update a specific lending record**  
  `PATCH /lending-records/{id}/`

- **Delete a specific lending record**  
  `DELETE /lending-records/{id}/`

## Return Transaction Endpoints

- **List all return transactions**  
  `GET /return-transactions/`

- **Create a new return transaction**  
  `POST /return-transactions/`

- **Retrieve a specific return transaction**  
  `GET /return-transactions/{id}/`

- **Update a specific return transaction**  
  `PUT /return-transactions/{id}/`

- **Partially update a specific return transaction**  
  `PATCH /return-transactions/{id}/`

- **Delete a specific return transaction**  
  `DELETE /return-transactions/{id}/`

## Penalty Endpoints

- **List all penalties**  
  `GET /penalties/`

- **Create a new penalty**  
  `POST /penalties/`

- **Retrieve a specific penalty**  
  `GET /penalties/{id}/`

- **Update a specific penalty**  
  `PUT /penalties/{id}/`

- **Partially update a specific penalty**  
  `PATCH /penalties/{id}/`

- **Delete a specific penalty**  
  `DELETE /penalties/{id}/`

## Payment Endpoints

- **List all payments**  
  `GET /payments/`

- **Create a new payment**  
  `POST /payments/`

- **Retrieve a specific payment**  
  `GET /payments/{id}/`

- **Update a specific payment**  
  `PUT /payments/{id}/`

- **Partially update a specific payment**  
  `PATCH /payments/{id}/`

- **Delete a specific payment**  
  `DELETE /payments/{id}/`

## Authentication

This project uses JWT (JSON Web Tokens) for authentication.

### Authentication Endpoints (Djoser)

- **Register a new user**  
  `POST /auth/users/`

- **Obtain authentication token**  
  `POST /auth/token/`

- **Obtain JWT token**  
  `POST /auth/jwt/create/`

- **Refresh JWT token**  
  `POST /auth/jwt/refresh/`

## Admin Interface

### Admin Dashboard

- **Access the admin dashboard**  
  `GET /admin/`  
  Log in using the superuser credentials created earlier.

## API Access

Once authenticated, include the JWT token in the Authorization header for subsequent requests:

```
Authorization: Bearer <your-jwt-token>

```
