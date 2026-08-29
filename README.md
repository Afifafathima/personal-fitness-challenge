# Personal Fitness Challenge Web Platform

A full-stack web application that helps users participate in fitness challenges, track their progress, monitor fitness data, and interact with trainers. The platform also provides trainer management and administrative moderation features.

## Live Demo

[Open the deployed application](https://personal-fitness-challenge.onrender.com/)

## Demo Credentials

The deployed application includes demo accounts for exploring the different roles.

### Admin
Email: `demo-admin@example.com`
Password: `your-demo-password`

### Trainer
Email: `demo-trainer@example.com`
Password: `your-demo-password`

### User
Email: `demo-user@example.com`
Password: `your-demo-password`

> These accounts are provided only for demonstration purposes.

Admin
  └── approved Demo Trainer

Demo Trainer
  └── has created challenges

Demo User
  └── can see and join those challenges

## Overview

The Personal Fitness Challenge Web Platform was developed to provide a centralized platform for users, fitness trainers, and administrators.

The application supports three main roles:

* **Users** — browse and join fitness challenges, track progress, log calories and weight, view leaderboards, and manage their profiles.
* **Trainers** — create and manage fitness challenges, view participation statistics, and maintain their trainer profiles.
* **Administrators** — review trainer registrations, manage challenges, and handle reported challenges.

## Key Features

### User Features

* User registration and login
* Personalized dashboard
* Browse fitness challenges
* Join and leave challenges
* Track challenge progress
* Daily fitness streak tracking
* Weight tracking and history
* Calorie logging and statistics
* User leaderboard
* Trainer discovery and trainer profiles
* Profile management

### Trainer Features

* Trainer registration
* Certificate submission
* Trainer approval workflow
* Trainer dashboard
* Create and edit challenges
* Challenge participation statistics
* Trainer leaderboard
* Trainer profile management
* Activity tracking

### Administrator Features

* Administrator dashboard
* Review pending trainer registrations
* Trainer approval
* Challenge management
* Challenge report management
* Moderation of reported content

## Technology Stack

**Frontend**

* HTML
* CSS
* JavaScript
* Tailwind CSS
* Chart.js

**Backend**

* Python
* Django

**Database**

* SQLite
* Django ORM

**Architecture**

* Django views
* Session-based authentication
* JSON APIs for dynamic frontend data
* Database-backed application state

## Application Architecture

The application follows a frontend-backend architecture:

```text
Browser
   │
   ▼
HTML / CSS / JavaScript
   │
   │ HTTP requests / JSON APIs
   ▼
Django Backend
   │
   ├── Authentication & Sessions
   ├── User Management
   ├── Trainer Management
   ├── Challenge Management
   ├── Progress Tracking
   ├── Fitness Statistics
   └── Moderation
   │
   ▼
Django ORM
   │
   ▼
SQLite Database
```

## Database Models

The backend contains models representing the main application entities, including:

* User
* Trainer
* Challenge
* JoinChallenge
* Activity
* Report
* WeightLog
* CalorieLog

These models allow the platform to store users, trainer information, challenges, participation, progress, fitness logs, activities, and reports.

## API Functionality

The backend exposes APIs for functionality such as:

* Challenge retrieval and creation
* Joining challenges
* Challenge reporting
* User and trainer statistics
* User and trainer profiles
* Challenge progress
* Weight history
* Calorie statistics
* User and trainer leaderboards
* Trainer approval workflows

## Authentication & Authorization

The application uses Django sessions to maintain logged-in users and determine their roles.

Different application flows are provided for:

* User
* Trainer
* Administrator

Trainer challenge creation also includes an approval check so that an unapproved trainer cannot create challenges.

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Afifafathima/personal-fitness-challenge.git
cd personal-fitness-challenge/fitness_app
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Project Structure

```text
personal-fitness-challenge/
│
├── fitness_app/
│   ├── manage.py
│   ├── core/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── tests.py
│   │   └── migrations/
│   │
│   ├── fitness_app/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── templates/
│       ├── user/
│       ├── trainer/
│       ├── admin/
│       └── signup/
│
├── css/
├── js/
├── components/
├── admin/
├── trainer/
├── user/
└── README.md
```

## What I Learned

Through this project, I worked with:

* Full-stack web application development
* Django backend development
* Database modeling using Django ORM
* API development
* Session-based authentication
* Role-based application flows
* CRUD operations
* Data aggregation and statistics
* Frontend-backend integration
* JavaScript API requests
* Dashboard development
* Git and GitHub

## Future Improvements

Potential improvements include:

* Migrating from SQLite to PostgreSQL for production
* Expanding automated test coverage
* Adding stronger role-based authorization
* Improving API validation and error handling
* Production deployment using a cloud platform
* Adding automated CI/CD
* Introducing personalized recommendations and analytics
* Improving frontend architecture and component reuse
