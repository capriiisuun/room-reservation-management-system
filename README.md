# 🏢 Room Reservation Management System

A web application built with Django and Python to manage room reservations and simplify the organization of shared spaces.

## 🎯 Project Objectives

- Manage rooms and their availability.
- Create and track room reservations.
- Organize reservation information in a centralized application.
- Provide a web interface for managing room bookings.
- Simplify the administration of rooms and reservations.

## 🛠️ Technologies

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript, Django Templates
- **Database:** SQLite (development)
- **Version Control:** Git and GitHub

## ✨ Features

- Room and reservation management.
- Reservation information management.
- Web-based interface.
- Django application architecture.
- Database integration through Django ORM.

*The features listed above should be adjusted to match the functionality implemented in the source code.*

## 📂 Project Structure

```text
room-reservation-management-system/
├── manage.py
├── app2/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── test2/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/capriiisuun/room-reservation-management-system.git
cd room-reservation-management-system
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Django

```bash
pip install django
```

If a `requirements.txt` file is available, install all project dependencies instead:

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

Open your browser at:

http://127.0.0.1:8000/

## 🖼️ Screenshots

Screenshots of the application interface can be added here to demonstrate the room management and reservation workflows.

## 🔒 Security Notes

- Keep secret keys and credentials out of the repository.
- Use environment variables for sensitive configuration.
- Do not publish databases containing personal or confidential information.
- Configure Django's production settings before deployment.

## 👩‍💻 Author

**Alaa Elkorchi**

AI & Data Science Engineering Student — EMSI

GitHub: [@capriiisuun](https://github.com/capriiisuun)

---

⭐ Feel free to explore this repository!
