# Customer Management App using Django, Django Rest Framework 

## 📚 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Running the Application Without Docker](#running-the-application-without-docker)
  - [Running the Application With Docker Compose](#running-the-application-with-docker-compose)
- [APIs](#apis)
- [Architecture and Design Patterns](#architecture-and-design-patterns)
  - [Clean Architecture + Repository Pattern](#1-clean-architecture--repository-pattern)
  - [Factory Pattern for Dependency Management](#2--factory-pattern-for-dependency-management)
  - [Service-Oriented Structure](#3--service-oriented-structure)
  - [Singleton Pattern](#4-singleton-pattern)
- [Database Diagram](#database-diagram)
- [Class Diagram And Architecture Diagram](#class-diagram-and-architecture-diagram)
- [Assumptions and Decisions](#assumptions-and-decisions)
  - [Application Level](#application-level)
  - [Usecase Level](#-usecase-level)


---

# Overview
This project is a Customer Management Application developed using Django and Django REST Framework. It enables users to register, log in, create customer records, view them on a dashboard, edit/delete each record, and log out securely.

The project is implemented in two layers:

- **RESTful API Layer** – `Built using Django REST Framework, this layer provides a set of RESTful APIs for managing customer objects. It supports secure login/logout using JWT (**djangorestframework-simplejwt**) and performs all customer CRUD operations in a REST-compliant manner.`
- **Web Interface Layer (MVT)** – `A user-facing interface built with Django templates, leveraging Django's Model-View-Template architecture. This allows users to interact with the system via web pages for login, customer creation, dashboard viewing, and logout, with UI styled using Bootstrap 5.`

This dual-layered structure demonstrates both API-first development and traditional server-rendered web application design using Django.


## Tech Stack
- **FrontEnd**: HTML, CSS, Bootstrap 5, Django Templates – for building responsive and clean user interfaces.
- **Django**: Serves as both the backend framework and template engine for frontend rendering.
- **Django REST Framework + OpenAPI/Swagger**: For building and documenting RESTful APIs.
- **Database**: Uses SQLite by default for development; easily configurable to use PostgreSQL, MySQL, or other relational databases.
- **Docker**: Containerizes the application for consistent environments and simplified deployment.
- **Git & GitHub**: Git for version control and GitHub for code hosting and collaboration.


## Project Structure

```
CustomerManagementApp/
├── CustomerManagementApp/              # Main project configuration
│   ├── settings.py                     # Project settings
│   ├── urls.py                         # Main URL configuration
│   ├── wsgi.py                         # WSGI configuration
│   ├── asgi.py                         # ASGI configuration
│   ├── middlewares.py                  # Custom middleware
│   ├── exceptions.py                   # Custom exceptions
│   ├── renderers.py                    # Custom renderers
│   └── logging_filters.py              # Logging filters
│
├── customers/                          # Customer management app
│   ├── domain/                         # Domain layer (Clean Architecture)
│   │   ├── interfaces/                 # Abstract interfaces
│   │   │   └── customer_repository.py  # Repository interface definitions
│   │   ├── services.py                 # Business logic services
│   │   └── service_factory.py          # Service factory for dependency injection
│   │
│   ├── interface/                      # Interface layer
│   │   ├── apis.py                     # REST API endpoints
│   │   ├── views.py                    # Web interface views
│   │   ├── forms.py                    # Form definitions
│   │   ├── serializers.py              # API serializers
│   │   ├── urls.py                     # API URL routing
│   │   └── view_urls.py                # Web URL routing
│   │
│   ├── repositories/                   # Data access layer
│   │   ├── respository.py              # Repository implementations
│   │   ├── repo_factories.py           # Repository factory
│   │   ├── querysets.py                # Custom querysets
│   │   ├── selectors.py                # Query selectors
│   │   └── entities.py                 # Data entities
│   │
│   ├── migrations/                     # Database migrations
│   ├── models.py                       # Customer models
│   ├── admin.py                        # Admin configurations
│   ├── tests.py                        # Test cases
│   └── apps.py                         # App configuration
│
├── users/                             # User management app
│   ├── apis/                          # API endpoints
│   ├── urls/                          # URL configurations
│   ├── migrations/                    # Database migrations
│   ├── models.py                      # User models
│   ├── views.py                       # View functions
│   ├── forms.py                       # Form definitions
│   ├── serializers.py                 # API serializers
│   ├── services.py                    # Business logic
│   ├── admin.py                       # Admin configurations
│   ├── tests.py                       # Test cases
│   └── apps.py                        # App configuration
│
├── common/                            # Shared utilities
├── templates/                         # HTML templates
├── logs/                             # Application logs
├── manage.py                         # Django management script
└── db.sqlite3                        # SQLite database
```


## Getting Started

### Prerequisites
- **Python 3.8+**
- **Docker and Docker Compose** (if running in Docker)

### Running the Application Without Docker
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/customer-management.git
    cd customer-management
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```bash
    python manage.py migrate
    ```

   if error is ```no such table: mainapi_customer```
    ```bash    
    python manage.py makemigrations mainapi
    python manage.py migrate
    ```

4. Run the development server:
    ```bash
    python manage.py runserver
    ```

5. Access the application at `http://127.0.0.1:8000`.

### Running the Application With Docker Compose
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/customer-management.git
    cd customer-management
    ```

2. Start the application with Docker Compose:
    ```bash
    docker-compose up --build
    ```

3. Access the application at `http://127.0.0.1:8000`.

To stop the application:
```bash
docker-compose down
```

## APIs
- **`api/v1/user/register/`** -- user registraion
- **`api/v1/user/token/`** -- user login via API
- **`api/v1/user/token/refresh/`** -- refresh user token
- **`api/v1/customers/add/`** -- customer add api
- **`api/v1/customers/fetch-all/`** -- customer add api, paginated response
- **`api/v1/customers/<id>/update/`** -- customer update api
- **`api/v1/customers/<id>/delete/`** -- customer delete api
- **`api/v1/user/logout/`** -- user logout api - (blacklist refresh token)



[//]: # (## 🧱 Architecture & Design Patterns)
## Architecture and Design Patterns
This project demonstrates multiple architectural approaches based on application context:

### 🧩 Customers App
### 1. Clean Architecture + Repository Pattern

The customers app is designed following the principles of Clean Architecture, ensuring a modular and scalable codebase. It is structured into the following layers:

   - **Domain Layer** : Contains business entities, service classes, and abstract repository interfaces. This layer is framework-agnostic and focused solely on business rules.

   - **Repository Layer** : Includes concrete repository implementations using the Django ORM and querysets. It implements the abstract interfaces defined in the domain.

   - **Interface Layer** : Comprises Django REST Framework views, serializers, and MVT views. It acts as a bridge between user input and domain logic, ensuring separation of concerns.

- This design enables unit testing, decouples the business logic from the framework, and supports better maintainability.

### 2.  🏭 Factory Pattern for Dependency Management

To maintain inversion of control and support modularity, factory classes are used to instantiate service and repository objects:
   - Repository Factories instantiate concrete repository implementations based on abstract interfaces defined in the domain layer.
   - Service Factories create service objects with injected repository dependencies, ensuring that services remain decoupled from their instantiation logic.

This approach:
   - Promotes loose coupling between layers.
   - Makes testing easier by allowing mock dependencies.
   - Supports future scalability (e.g., switching DB backends or integrating external services).

### 👤 Users App

### 3.  – Service-Oriented Structure

The users app uses a simpler service-layer architecture. Business logic related to user registration is encapsulated in service functions, which are called from views or DRF endpoints.

This hybrid approach keeps complexity low where it's unnecessary while applying structured separation in areas (like customer management) that benefit from it.

### 4. Singleton Pattern
- Database Connection: Django maintains a single persistent database connection per thread or process (depending on the server), effectively treating the database connection as a singleton.
- Settings Module: The `settings.py` file acts as a singleton configuration provider, ensuring consistent application settings are available globally throughout the project.
- Logging: Django uses a centralized logging configuration defined in `settings.py`. This setup ensures a single, shared logging interface is used across the entire application.

## Database Diagram
- https://dbdiagram.io/d/Customer-682188cf5b2fc4582f273a20

## Class Diagram And Architecture Diagram

#### Class Diagram
 - https://drive.google.com/file/d/12xVB04zkG4EQgbkXyZUWQKPc_atzNFhu/view?usp=sharing

#### Architecture Diagram
- https://drive.google.com/file/d/1FUdsnkleGR7PRCNWbAASyuY6tsIC_rSa/view?usp=sharing



## Assumptions and Decisions

### Application Level 
1. **SQLite Database**:
   - SQLite is used initially as a lightweight, embedded database for simplicity and ease of development. The application can be easily reconfigured to use production-ready databases like PostgreSQL or MySQL by updating the database settings in the configuration.
2. **JWT Authentication**:
   -  **djangorestframework-simplejwt** is a JSON Web Token (JWT) authentication backend for Django REST Framework. It covers common JWT use cases with a secure and minimal set of default features. In this application, it is used for authenticating users by issuing access and refresh tokens, as well as blacklisting tokens upon logout.
3. **OpenAPI Specification/Swagger**:
   - **drf_yasg** is used in this project to provide and OpenAPI Specification documentation to the users
4. **phonenumber_field**:
   - This external django library is used for validating the phone number of user.
### 🧩 Usecase Level
The application supports two modes of interaction:
- Web Flow via Django templates (server-rendered views).
- API Flow via Django REST Framework (for frontend integration like React, or API consumers).
- User Authentication Flow:
    - Users can register and log in using either the web interface or REST APIs.
    - Web-based login uses Django's session-based auth.
    - API login uses JWT (access and refresh tokens) via djangorestframework-simplejwt.
- Web Flow Details:
    - Upon visiting the root URL, the user is redirected to a login page. If not already registered, they may register.
    - After logging in, the user is directed to the Customer Dashboard, where they can:
        - View a paginated list of customers.
        - Create, edit, and soft-delete customer records.
        - Logout is available via the navbar on all pages.
- REST API Flow:
    - Separate endpoints are exposed for:
        - User Registration
        - JWT Token Generation (Login)
        - Customer CRUD Operations
        - Token Blacklisting (Logout)
        - All APIs follow a consistent JSON response structure with status, message, errors, and data fields.
- Data Validations:
    - Date of Birth: Ensures customer age is between 13 and 100 years.
    - Phone Number: Must be unique; duplicate entries are rejected with a meaningful error.
- Soft Deletion:
    - Customers are not hard-deleted from the database. Instead, a flag is used to mark them as inactive.

- API Response Format:
    ##### 
        {"status": "Success",
        "message": "Customers Fetch Successfully",
        "errors": [],
        "data": {}
        }
