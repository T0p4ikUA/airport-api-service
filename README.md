# ✈️ Airport API Service

RESTful API service for airport and flight management, built with **Django REST Framework (DRF)** and containerized with **Docker**.

---

## 🛠Technologies & Tools
- **Python 3.12** / **Django 5.x** / **Django REST Framework**
- **PostgreSQL** (Database)
- **Docker & Docker Compose** (Containerization)
- **JWT Authentication** (SimpleJWT)
- **Swagger/Redoc** (API Documentation)

---

## Features
- **Airport & Route Management**: Manage airports, cities, and flight routes with calculated distances.
- **Fleet Management**: Track airplane types, individual airplanes, seating capacities (rows and seats in a row).
- **Crew Management**: Assign and manage flight crews.
- **Flight Scheduling**: Create flights, assign routes, airplanes, and crew members.
- **Booking System**: Users can place orders and purchase tickets for specific seats on flights.
- **Authentication**: Custom user model with secure token-based authentication.

---

## Quick Start with Docker (Recommended)

Make sure you have **Docker** and **Docker Compose** installed on your machine.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/T0p4ikUA/airport-api-service.git](https://github.com/T0p4ikUA/airport-api-service.git)
   cd airport-api-service
Configure environment variables:
Create a .env file in the root directory based on .env.sample:

Bash
cp .env.sample .env
(You can keep the default values for local development)

Build and run containers:

Bash
docker-compose up --build -d
Run migrations:

Bash
docker-compose exec app python manage.py migrate
Load initial sample data (Fixtures):

Bash
docker-compose exec app python manage.py loaddata fixture.json
Create a superuser (for Django Admin & testing):

Bash
docker-compose exec app python manage.py createsuperuser
API is up and running!
Open your browser or API client at: http://127.0.0.1:8000/

Local Installation (Alternative)
If you prefer running the app without Docker locally:

Clone the repository & create a virtual environment:

Bash
git clone [https://github.com/T0p4ikUA/airport-api-service.git](https://github.com/T0p4ikUA/airport-api-service.git)
cd airport-api-service
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt
Set up your .env file and configure your local PostgreSQL database.

Run migrations:

Bash
python manage.py migrate
Load initial sample data:

Bash
python manage.py loaddata fixture.json
Create a superuser:

Bash
python manage.py createsuperuser
Run the development server:

Bash
python manage.py runserver
