# SkillSpark

SkillSpark is an advanced educational and employee management platform built using Django and Django REST Framework for the backend, React.js with Redux Toolkit for the frontend, and PostgreSQL as the database. It enables companies to efficiently manage their workforce, organize internal training, quizzes, and courses, while employees have the opportunity to improve their skills through personalized educational resources.

The platform offers an intuitive user interface, detailed analytics, and multi-role user support, including administrators, companies, and employees. It leverages JWT-based authentication, PDF generation for detailed reports. The goal is to enhance employee productivity and competencies through interactive learning, evaluation, and performance tracking.

## Table of Contents
- [Project Architecture](#project-architecture)
- [Pre-required Installation](#pre-required-installation)
- [Installation Guide](#installation-guide)
- [Features](#features)
- [Libraries and Tools](#libraries-and-tools)

## Project Architecture

### Backend Structure

```
api/                                      # Backend (Django REST Framework)
|-- api/                                  # Main Django project settings
|   |-- __init__.py
|   |-- asgi.py
|   |-- settings.py                       # Django settings (database, authentication, middleware)
|   |-- urls.py                           # Root URL configuration
|   |-- wsgi.py
|
|-- authentication/                       # User authentication and management
|   |-- models.py                         # User model (Admin, Company, Employee)
|   |-- serializers.py                    # User serializers
|   |-- views.py                          # User authentication views (login, registration)
|   |-- urls.py                           # Authentication API routes
|   |-- tests.py                          # Unit tests for authentication
|
|-- dashboard/                            # Dashboard and analytics
|   |-- views.py                          # Admin, Company, and Employee dashboard logic
|   |-- urls.py
|   |-- tests.py
|
|-- password_reset/                       # Password reset functionality
|   |-- serializers.py                    # Password reset serializers
|   |-- views.py                          # Password reset views
|   |-- urls.py                           # Password reset API routes
|   |-- tests.py                          # Tests for password reset
|
|-- quizzes/                              # Quiz and training management
|   |-- models.py                         # Quiz, Questions, Answers models
|   |-- serializers.py                    # Quiz API serializers
|   |-- views.py                          # Quiz views (create, take, results)
|   |-- urls.py                           # Quiz API routes
|   |-- tests.py                          # Unit tests for quizzes
|
|-- user_management/                      # Employee and company user management
|   |-- serializers.py
|   |-- views.py
|   |-- urls.py
|   |-- tests.py
|
|-- templates/                            # Email templates
|   |-- password_reset_email.html
|   |-- quiz_failed.html
|   |-- quiz_passed.html
|   |-- welcome_email.html
|
|-- manage.py                             # Django management script
|-- requirements.txt                      # Python dependencies
```

### Frontend Architecture

```
app/
|-- public/                                   # Static files (HTML, images, etc.)
|-- src/                                      # Source code
|   |-- components/                           # React components
|   |   |-- Admin/                            # Admin-related components
|   |   |-- AdminQuizzes.js                   # Admin quiz management
|   |   |-- AdminStatistics.js                # Admin statistics dashboard
|   |   |-- BarCard.js                        # Bar chart component
|   |   |-- Company/                          # Company-related components
|   |   |-- CompanyProfile.js                 # Company profile management
|   |   |-- CompanyProfileEdit.js             # Edit company profile
|   |   |-- CompanyStatistics.js              # Company analytics
|   |   |-- ConfirmPopup.js                   # Reusable confirmation dialog
|   |   |-- CreateUserPopup.js                # Popup for user creation
|   |   |-- DonutCard.js                      # Donut chart component
|   |   |-- Employee/                         # Employee-related components
|   |   |-- EmployeeManagement.js             # Employee management page
|   |   |-- EmployeePassedQuizzes.js          # Passed quizzes list
|   |   |-- EmployeePopup.js                  # Popup for employee actions
|   |   |-- EmployeeProfile.js                # Employee profile
|   |   |-- EmployeeProfileEdit.js            # Edit employee profile
|   |   |-- EmployeeQuizDetail.js             # Quiz details for employees
|   |   |-- EmployeeQuizzes.js                # List of quizzes for employees
|   |   |-- EmployeeStatistics.js             # Employee statistics page
|   |   |-- Footer.js                         # Footer component
|   |   |-- ForgotPassword.js                 # Forgot password page
|   |   |-- GoTop.js                          # Scroll to top button
|   |   |-- HamburgerMenu.js                  # Mobile menu component
|   |   |-- LandingPage.js                    # Landing page
|   |   |-- Language.js                       # Language selection component
|   |   |-- Loading.js                        # Loading indicator
|   |   |-- Login.js                          # Login page
|   |   |-- Logout.js                         # Logout functionality
|   |   |-- NotFound.js                       # 404 page
|   |   |-- PassedQuizzes.js                  # Passed quizzes component
|   |   |-- PieCard.js                        # Pie chart component
|   |   |-- QuestionForm.js                   # Form for quiz questions
|   |   |-- QuizCard.js                       # Individual quiz card
|   |   |-- QuizForm.js                       # Form for creating quizzes
|   |   |-- QuizTaking.js                     # Quiz taking interface
|   |   |-- Quizzes.js                        # Main quizzes page
|   |   |-- Register.js                       # Registration page
|   |   |-- ResetPassword.js                  # Reset password page
|   |   |-- Theme.js                          # Theme toggle (light/dark mode)
|   |   |-- ToastNotification.js              # Notifications
|   |   |-- TopBar.js                         # Navigation top bar
|   |   |-- Unauthorized.js                   # Unauthorized access page
|   |   |-- UserCard.js                       # User profile card
|   |   |-- UserManagement.js                 # User management page
|
|   |-- locales/                              # Localization files
|   |   |-- bs/global.json                    # Bosnian translations
|   |   |-- en/global.json                    # English translations
|
|   |-- middleware/                           # Middleware functions
|   |   |-- index.js                          # Middleware entry point
|   |   |-- ProtectedRoute.js                 # Route protection middleware
|   |   |-- RedirectHome.js                   # Home redirection logic
|
|   |-- store/                                # Redux store configuration
|   |   |-- index.js                          # Store entry point
|   |   |-- languageSlice.js                  # Language settings state
|   |   |-- themeSlice.js                     # Theme settings state
|
|   |-- styles/                               # Stylesheets
|   |   |-- _variables.scss                    # Global SCSS variables
|
|   |-- App.js                                # Main React component
|   |-- App.scss                              # Main styles
|   |-- index.js                              # Application entry point
|   |-- index.scss                            # Entry point styles
|   |-- i18n.js                               # Internationalization configuration
|
|-- package.json                              # NPM dependencies
|-- package-lock.json                         # NPM lock file
```

### Pre-required Installation

#### Backend:

1) Python (v3.9 or higher) - https://www.python.org/downloads/
2) PostgreSQL (v13 or higher) - https://www.postgresql.org/download/
3) Django (v4.x) - Included in requirements.txt

#### Frontend:

1) Node.js (v16 or higher) - https://nodejs.org/en/download
2) React.js - Installed via package.json

### Installation Guide


#### Backend Installation:

1) Clone the repository:
```
git clone https://github.com/Kalaba01/skill-spark.git
cd skill-spark/api
```
2) Install dependencies:
```
pip install -r requirements.txt
```
3) Configure environment variables in .env:
```
SECRET_KEY=your_secret_key

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port

DEBUG=False

EMAIL_USER=your_email_user
EMAIL_PASS=your_email_password
SMTP_FROM=your_email_from_address

```
4) Apply database migrations:
```
python manage.py migrate
```
5) Create a superuser:
```
python manage.py createsuperuser
```
6) Run the backend server:
```
python manage.py runserver
```
The backend API will be available at http://localhost:8000


#### Frontend Installation:
1) Navigate to the frontend directory:
```
cd ../app
```
2) Install dependencies:
```
npm install
```
3) Start the frontend server:
```
npm start
```
The application will be available at http://localhost:3000

## Features

### Admin:
- Manage companies and employees
- View platform statistics (total quizzes, employees, companies)

### Company:
- Profile Management
- Manage employees (create, update, delete)
- Create and manage quizzes
- Generate PDF reports for employees

### Employee:
- Profile Management
- Take quizzes assigned by the company
- View results and track progress


## Libraries and Tools

| Libary/Tool             | Version | Purpose                      |
|-------------------------|---------|------------------------------|
| Backend                 |         |                              |
| Django                  | 4.x     | Backend framework            |
| Django REST Framework   | 3.x     | API framework for Django     |
| PostgreSQL              | 13+     | Database                     |
| djangorestframework-jwt | 5.x     | JWT-based authentication     |
| pdfkit                  | 1.x     | PDF generation               |
| Frontend                |         |                              |
| React.js                | 19.0.0  | Frontend framework           |
| React Router DOM        | 7.1.3   | Routing for React apps       |
| Redux Toolkit           | 2.5.1   | State management             |
| React Redux             | 9.2.0   | React bindings for Redux     |
| Axios                   | 1.7.9   | HTTP client for API requests |
| i18next                 | 24.2.2  | Internationalization support |
| Chart.js                | 4.4.8   | Data visualization library   |
| Sass                    | 1.83.4  | Styling preprocessor         |
