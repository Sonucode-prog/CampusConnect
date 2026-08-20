![Landing Page](cc_landingpage.png)
# COMPUSCONNECT — Project Overview

**COMPUSCONNECT** is a full-stack web application designed to provide a centralized platform for managing interactions between students, companies, colleges, and administrators. The system provides role-based dashboards, secure authentication, opportunity management, application tracking, and administrative features through a modern web interface.

## 🛠️ Technologies Used

### Frontend

* **Vue.js** — Used to build the interactive and component-based user interface.
* **Bootstrap** — Used for responsive layouts, navigation bars, cards, forms, buttons, and overall UI styling.
* **Axios** — Used to communicate with the backend REST APIs.
* **Vue Router** — Used for client-side navigation and protected routes.
* **Vuex** — Used for centralized state management.

### Backend

* **Python** — Primary backend programming language.
* **FastAPI** — Used to develop RESTful APIs and backend services.
* **SQLAlchemy** — Used as the ORM for database interaction and model management.
* **Pydantic** — Used for request validation and data schemas.
* **JWT Authentication** — Used for secure authentication and authorization.
* **Uvicorn** — Used as the ASGI server to run the FastAPI application.

### Database & Background Services

* **Relational Database** — Used to store users, companies, students, opportunities, applications, and other application data.
* **Redis** — Used as a message broker/cache for background processing.
* **Celery** — Used to execute asynchronous/background tasks.

### Development Tools

* **Git & GitHub** — Used for version control and project management.
* **REST APIs** — Used for communication between the Vue.js frontend and FastAPI backend.

---

## ⭐ Key Features

### 🔐 Authentication & Authorization

* User login and registration.
* JWT-based authentication.
* Secure access to protected APIs.
* Role-based authorization.
* Different permissions and dashboards based on user roles.

### 👨‍💼 Admin Dashboard

* Centralized admin dashboard.
* View important platform statistics.
* Manage and monitor users and platform activities.
* Access administrative APIs through protected routes.

### 🏢 Company Management

* Company-specific dashboard.
* Manage company information.
* Create and manage opportunities.
* View and manage student applications.
* Track recruitment-related activities.

### 🎓 Student Management

* Student-specific dashboard.
* View available opportunities.
* Apply for opportunities.
* Track application status.
* Manage student profile information.

### 🏫 College Management

* College/institute-related functionality.
* Manage college information.
* Access relevant opportunities and application information.

### 📊 Dashboard & Data Management

* Role-specific dashboards.
* Dynamic data retrieved through REST APIs.
* CRUD operations for major application entities.
* Centralized state management using Vuex.

### 🔄 API Integration

* Frontend communicates with the backend using Axios.
* RESTful API architecture.
* Protected API requests using JWT tokens.
* Backend request validation using Pydantic.

### ⚙️ Background Processing

* Asynchronous task processing using Celery.
* Redis used as the message broker.
* Background jobs can run independently from API requests.

### 📱 Responsive UI

* Responsive interface built using Bootstrap.
* Reusable Vue.js components.
* Navigation and page routing using Vue Router.

---

## 🔑 Main Technical Highlights

The project demonstrates practical implementation of:

* Full-stack application architecture
* Vue.js frontend development
* FastAPI REST API development
* JWT authentication
* Role-based access control (RBAC)
* SQLAlchemy ORM
* Relational database management
* Axios API integration
* Vue Router
* Vuex state management
* Redis and Celery background processing
* CRUD operations
* Responsive web design
* Git/GitHub version control
