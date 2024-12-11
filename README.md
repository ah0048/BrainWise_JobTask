# Employee Management System
# Backend

This is the backend for an Employee Management System built with Django and Django REST Framework (DRF). The system manages companies, departments, and employees, and includes role-based access control for different user roles (Admin, Manager, Employee).

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
3. [API Documentation](#api-documentation)
    - [Authentication](#authentication)
    - [Companies](#companies)
    - [Departments](#departments)
    - [Employees](#employees)
4. [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)

## Features
- User authentication using token-based authentication (via Django Rest Framework Token Authentication).
- CRUD operations for Companies, Departments, and Employees.
- Role-based access control for:
  - **Admin:** Full access to all CRUD operations.
  - **Manager:** CRUD operations on employees, view/edit access to departments and companies.
  - **Employee:** Read-only access to all resources.

## Installation

### Prerequisites
- Python 3.x
- Django 5.x
- Django REST Framework (DRF)
- SQLite (default database)

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/ah0048/BrainWise_JobTask
    cd BrainWise_JobTask
    ```

2. Create a virtual environment:
    ```bash
    cd backend
    python -m venv env
    source env/bin/activate  # On Windows, use 'env\Scripts\activate'
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser (for Admin access):
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```
    The backend should now be running on [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## API Documentation

### Authentication
#### Login
- **URL:** `/api/login/`
- **Method:** `POST`
- **Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "password123"
    }
    ```
- **Response:**
    ```json
    {
      "token": "your-token-here"
    }
    ```
    **Description:** Authenticates the user and returns a token for authentication in subsequent API calls.

### Companies
#### Get all companies
- **URL:** `/api/companies/`
- **Method:** `GET`
- **Permissions:** Admin, Manager, Employee
- **Response:**
    ```json
    [
      {
        "id": 1,
        "name": "Company 1",
        "num_departments": 3,
        "num_employees": 15
      },
      ...
    ]
    ```

#### Get a single company
- **URL:** `/api/companies/{id}/`
- **Method:** `GET`
- **Permissions:** Admin, Manager, Employee

#### Create a company
- **URL:** `/api/companies/create/`
- **Method:** `POST`
- **Permissions:** Admin
- **Body:**
    ```json
    {
      "name": "New Company",
      "num_departments": 0,
      "num_employees": 0
    }
    ```

#### Update a company
- **URL:** `/api/companies/{id}/update/`
- **Method:** `PUT`
- **Permissions:** Admin, Manager
- **Body:**
    ```json
    {
      "name": "Updated Company Name",
      "num_departments": 5,
      "num_employees": 20
    }
    ```

#### Delete a company
- **URL:** `/api/companies/{id}/delete/`
- **Method:** `DELETE`
- **Permissions:** Admin

### Departments
#### Get all departments
- **URL:** `/api/departments/`
- **Method:** `GET`
- **Permissions:** Admin, Manager, Employee

#### Get a single department
- **URL:** `/api/departments/{id}/`
- **Method:** `GET`
- **Permissions:** Admin, Manager, Employee

#### Create a department
- **URL:** `/api/departments/create/`
- **Method:** `POST`
- **Permissions:** Admin
- **Body:**
    ```json
    {
      "company": 1,
      "name": "New Department",
      "num_employees": 0
    }
    ```

#### Update a department
- **URL:** `/api/departments/{id}/update/`
- **Method:** `PUT`
- **Permissions:** Admin, Manager
- **Body:**
    ```json
    {
      "company": 1,
      "name": "Updated Department Name",
      "num_employees": 10
    }
    ```

#### Delete a department
- **URL:** `/api/departments/{id}/delete/`
- **Method:** `DELETE`
- **Permissions:** Admin

### Employees
#### Get all employees
- **URL:** `/api/employees/`
- **Method:** `GET`
- **Permissions:** Admin, Manager, Employee

#### Get a single employee
- **URL:** `/api/employees/{id}/`
- **Method:** `GET`
- **Permissions:** Admin, Manager, Employee

#### Create an employee
- **URL:** `/api/employees/create/`
- **Method:** `POST`
- **Permissions:** Admin, Manager
- **Body:**
    ```json
    {
      "company": 1,
      "department": 2,
      "status": "hired",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "mobile_number": "+123456789",
      "address": "123 Some Street",
      "designation": "Developer",
      "hired_on": "2023-01-01"
    }
    ```

#### Update an employee
- **URL:** `/api/employees/{id}/update/`
- **Method:** `PUT`
- **Permissions:** Admin, Manager
- **Body:**
    ```json
    {
      "status": "interview_scheduled",
      "address": "456 Another Street"
    }
    ```

#### Delete an employee
- **URL:** `/api/employees/{id}/delete/`
- **Method:** `DELETE`
- **Permissions:** Admin, Manager

## Role-Based Access Control (RBAC)
- **Admin:** Can perform any action on all resources (companies, departments, employees).
- **Manager:** Can perform CRUD operations on employees and view/edit companies and departments.
- **Employee:** Can only view the data of companies, departments, and employees. No modification permissions.
