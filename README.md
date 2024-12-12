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
    python -m venv venv
    source env/bin/activate  # On Windows, use 'env\Scripts\activate'
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run migrations:
    ```bash
    cd myproject
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

# Employee Management System - Frontend

## Introduction

The frontend of the Employee Management System is built using Vue.js. This system interacts with a Django REST Framework (DRF) backend to manage companies, departments, and employees, with role-based access control for different user roles (Admin, Manager, Employee). The system includes interactive pages for viewing, creating, editing, and deleting employees, departments, and companies, depending on the user's role.

## Table of Contents

- [Features](#features)
- [Folder Structure](#folder-structure)
- [Components](#components)
- [Routing](#routing)
- [State Management](#state-management)
- [Modals](#modals)
- [Role-Based Access Control](#role-based-access-control)
- [Form Handling](#form-handling)
- [Running the Application](#running-the-application)
- [API Integration](#api-integration)
- [Error Handling](#error-handling)
- [Assumptions](#assumptions)

## Features

- **CRUD Operations for Employees, Departments, and Companies**: Admin and Manager roles can create, read, update, and delete employees. Employees can only view their data and are restricted from modifying it. Role-based access ensures that only authorized users can perform certain actions.
- **Modals** for viewing and editing employee, department, and company information.
- **Dynamic forms** with validation, including select dropdowns for departments based on the selected company.
- **Status workflow** for employees, where only valid transitions are allowed based on the current status (e.g., from "Application Received" to "Interview Scheduled" or "Not Accepted").

## Folder Structure

Here is the structure of the frontend directory:

```bash
src/
├── assets/               # Static assets (images, icons, etc.)
├── components/           # Reusable components
│   ├── AppNavbar.vue     # Navbar component
├── views/                # Views representing different pages of the app
│   ├── EmployeePage.vue  # Employee management page
│   ├── CompanyPage.vue   # Company management page
│   ├── DepartmentPage.vue# Department management page
├── router/               # Vue Router for page navigation
│   └── index.js          # Routes and navigation logic
├── store/                # Vuex store (optional, if used)
│   └── index.js
├── App.vue               # Root Vue component
└── main.js               # Entry point of the app
```
## Components
1. AppNavbar.vue
This component is a reusable navigation bar across different pages. It provides links to the employee, department, and company pages, and shows different options based on the user's role (Admin, Manager, Employee).

2. EmployeeCard.vue
Displays a card for each employee, including their name, designation, and status. Includes buttons for viewing, editing, and deleting employees (depending on user role).

3. Modals
View Modal: Displays detailed information about an employee, including their company, department, status, and hired date.

Edit Modal: Allows users to edit an employee's information (name, email, mobile number, etc.). The status field is dynamically populated based on the employee's current status and workflow.

Create Modal: Allows users to create new employees, with dropdowns for selecting company and department.

## Routing
The application uses Vue Router for navigation. Here’s a breakdown of the routes:

/home - Displays the summary of companies, departments, and employees.

/employees - The page for managing employees, including viewing, editing, creating, and deleting employees.

/companies - The page for managing companies.

/departments - The page for managing departments.

/account - The page for viewing and editing the user's account details.

```bash
const routes = [
  {
    path: "/home",
    name: "HomePage",
    component: HomePage,
    beforeEnter: (to, from, next) => {
      if (!localStorage.getItem("token")) {
        next({ name: "LandingPage" });
      } else {
        next();
      }
    },
  },
  {
    path: "/employees",
    name: "EmployeePage",
    component: EmployeePage,
    beforeEnter: (to, from, next) => {
      if (!localStorage.getItem("token")) {
        next({ name: "LandingPage" });
      } else {
        next();
      }
    },
  },
  // Other routes for companies, departments, and account
];
```
## State Management
The application stores user data (such as authentication token and user role) in localStorage.

```bash
data() {
  return {
    userRole: localStorage.getItem("userRole"),
    token: localStorage.getItem("token"),
    employees: [],
    companies: [],
    departments: [],
  };
},
```
## Modals
Create, Edit, and View Modals
Create Modal: Used for adding new employees. It includes a form where the user selects the company and department. The department dropdown is dynamically populated based on the selected company.

Edit Modal: Allows for updating employee details, with fields that are pre-populated based on the selected employee's data.

View Modal: Displays employee details in read-only mode.

Role-Based Access Control
The application enforces role-based access control for certain actions. The following roles are defined:

Admin: Has full access to all CRUD operations.

Manager: Can create, read, update, and delete employees but cannot manage companies or departments.

Employee: Can only view data related to companies, departments, and employees.

Example of Role Checking
```bash
<v-if="userRole === 'admin' || userRole === 'manager'">
  <button @click="editEmployee(employee)" class="edit-button">Edit</button>
</v-if>
```
## Form Handling
Employee Creation
The form allows creating an employee with a dynamic department dropdown, which is enabled only after selecting a company. When the company is selected, the department dropdown is populated with departments related to that company.

```bash
<select id="company" v-model="form.company" @change="onCompanyChange" required>
  <option v-for="company in companies" :key="company.id" :value="company.id">{{ company.name }}</option>
</select>
<select id="department" v-model="form.department" :disabled="!form.company" required>
  <option v-for="dept in filteredDepartments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
</select>
```
Validation and Error Handling
Form validation is handled using Vue’s built-in required directive. For more advanced validation (such as checking the status transition), logic is implemented within the methods (e.g., ensuring that only valid status transitions are allowed).

## Running the Application
Install dependencies:

```bash
cd frontend
npm install
```
Run the application:

```bash
npm run serve
```
The app will be available at http://localhost:7070.

## API Integration
The frontend communicates with the backend via HTTP requests to the Django REST API. Common API calls include:

Get Employees: GET /employees/

Get Companies: GET /companies/

Create Employee: POST /employees/create/

Update Employee: PUT /employees/{id}/update/

Delete Employee: DELETE /employees/{id}/delete/

Each request includes an Authorization header with a token stored in localStorage:

```bash
const response = await fetch(`${process.env.VUE_APP_API_URL}/employees/`, {
  headers: {
    Authorization: `Token ${localStorage.getItem("token")}`,
  },
});
```
## Error Handling
The frontend handles errors using try...catch blocks and provides meaningful feedback to users. For example, if the employee creation fails, the user is notified with an alert message.

```bash
if (!response.ok) {
  const errorData = await response.json();
  alert(`Error creating employee: ${JSON.stringify(errorData)}`);
}
```
## Assumptions
User, Company, and Department Creation
The user creation, company creation, and department creation are assumed to be done via the Django Admin Panel, as the frontend and backend requirements do not specify their creation process. These resources are created and managed by an Admin via the admin panel, and users, companies, and departments are then accessible through the frontend for viewing and management by Admins and Managers.

## Role Management
Role-based access control (RBAC) is implemented in both the frontend and backend. Users with roles like Admin, Manager, and Employee are assigned specific permissions to create, update, delete, and view resources based on their role.
