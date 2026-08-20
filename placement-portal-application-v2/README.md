# COMPUSCONNECT

## Project Overview

COMPUSCONNECT is a web-based Campus Placement Management System designed to manage and simplify the placement process of an educational institution.

The system provides a centralized platform for three types of users: Admin, Student, and Company.

Students can browse and apply for approved job opportunities. Companies can post jobs and manage student applications. Administrators can approve companies and jobs and monitor the complete placement process.

---

## Features

### Admin

- Admin login and authentication
- Manage students
- Manage companies
- Approve or reject companies
- View job opportunities
- Approve or reject jobs
- Monitor student applications
- View placement records
- View placement statistics
- Generate placement reports

### Student

- Student registration and login
- Manage student profile
- Browse approved and open jobs
- View job details
- View company information
- Apply for jobs
- Track application status
- View placement details
- Export placement details as CSV

### Company

- Company registration and login
- Manage company profile
- Create job opportunities
- View posted jobs
- Track job approval status
- View student applications
- Update application status
- Manage selected students
- View placement records
- Export placement data as CSV

---

## Technology Stack

### Frontend

- Vue.js
- Vue Router
- Vite
- Axios
- JavaScript
- HTML5
- CSS3
- Bootstrap

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- SQLAlchemy

### Database

- SQLite

### Caching and Background Tasks

- Redis
- Celery
- Celery Beat

### Development Tools

- Git
- GitHub
- VS Code
- MailHog

---

## Project Structure

```text
COMPUSCONNECT/
│
├── backend/
│   ├── exports/
│   ├── instance/
│   │   └── ppa.db
│   ├── migrations/
│   ├── reports/
│   ├── templates/
│   ├── uploads/
│   │
│   ├── app.py
│   ├── cache_keys.py
│   ├── cache_utils.py
│   ├── cache.py
│   ├── celery_worker.py
│   ├── models.py
│   └── tasks.py
│
├── fronted_part/
│   ├── public/
│   │
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── router/
│   │   ├── views/
│   │   ├── App.vue
│   │   └── main.js
│   │
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── .gitignore
├── README.md
└── requirements.txt

## Installation and Setup

Follow the steps below to run COMPUSCONNECT on your local system.

### Prerequisites

Make sure the following software is installed:

- Python 3
- Node.js and npm
- Redis Server
- Git

---

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd COMPUSCONNECT
```

---

### 2. Create Python Virtual Environment

Create a virtual environment:

```bash
python -m venv env
```

Activate the virtual environment.

#### Windows

```bash
env\Scripts\activate
```

#### Linux / macOS

```bash
source env/bin/activate
```

---

### 3. Install Backend Dependencies

Install the required Python packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 4. Start the Flask Backend

Navigate to the backend directory:

```bash
cd backend
```

Run the Flask application:

```bash
python app.py
```

The backend server will run at:

```text
`${import.meta.env.VITE_API_URL}
```

Keep this terminal running.

---

### 5. Start Redis Server

Open a new terminal and start Redis:

```bash
redis-server
```

Verify that Redis is running:

```bash
redis-cli ping
```

Expected output:

```text
PONG
```

Keep the Redis server running.

---

### 6. Start Celery Worker

Open a new terminal.

Activate the Python virtual environment:

#### Windows

```bash
env\Scripts\activate
```

#### Linux / macOS

```bash
source env/bin/activate
```

Navigate to the backend directory:

```bash
cd backend
```

Start the Celery worker:

```bash
celery -A celery_worker.celery worker --loglevel=info
```

Keep the Celery worker running.

---

### 7. Start Celery Beat

Open another terminal.

Activate the Python virtual environment and navigate to the backend directory.

```bash
cd backend
```

Start Celery Beat:

```bash
celery -A celery_worker.celery beat --loglevel=info
```

Celery Beat handles scheduled and periodic tasks.

---

### 8. Install Frontend Dependencies

Open a new terminal and navigate to the frontend directory:

```bash
cd fronted_part
```

Install the required npm packages:

```bash
npm install
```

---

### 9. Start the Vue Frontend

Run the Vue development server:

```bash
npm run dev
```

The frontend application will usually run at:

```text
http://localhost:5173
```

Open the URL displayed in the terminal in your browser.

---

## Running the Complete Application

The following services should be running simultaneously:

| Service | Command |
|---|---|
| Flask Backend | `python app.py` |
| Redis Server | `redis-server` |
| Redis Server shutdown | `redis-cli shutdown` |
| Celery Worker | `celery -A celery_worker:celery_app worker --loglevel=info` |
| Celery Beat | `celery -A celery_worker:celery_app beat --loglevel=info` |
| Vue Frontend | `npm run dev` |

After starting all services, open:

```text
http://localhost:5173
```

The COMPUSCONNECT application is now ready to use.

---

## Development Email Server

MailHog is used to test email functionality during development.

Start MailHog from the backend directory according to your local MailHog executable configuration.

The MailHog web interface is generally available at:

| Runing MailHog | `./MailHog` | then go to below link
```text
http://localhost:8025
```

MailHog captures development emails without sending them to real email addresses.