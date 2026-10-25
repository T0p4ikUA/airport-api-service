# ✈️ Airport API Service

RESTful API service for airport and flight management, built with **Django REST Framework (DRF)** and containerized with **Docker**.

---

## Technologies & Tools
- **Python 3.12** / **Django 5.x** / **Django REST Framework**
- **PostgreSQL** (Database)
- **Docker & Docker Compose** (Containerization)
- **JWT Authentication** (`djangorestframework-simplejwt`)
- **Swagger/Redoc** (API Documentation via `drf-spectacular`)
- **Environment Management** (`python-dotenv`)

---

## Features
- **Airport & Route Management**: Manage airports, cities, and flight routes with unique constraints and validated distances.
- **Fleet Management**: Track airplane types, individual airplanes, and seating capacities (validated rows and seats in a row).
- **Crew Management**: Assign and manage flight crews.
- **Flight Scheduling**: Create flights, assign routes, airplanes, and crew members with strict arrival/departure time validation.
- **Booking System**: Users can place orders and purchase tickets for specific seats with atomic transactions preventing double-booking/race conditions.
- **Authentication**: Secure token-based authentication (JWT) with user registration, token refresh, and profile management endpoints (`/api/user/`).

---

## ⚙Environment Variables

Create a `.env` file in the root directory based on the provided `.env.sample`:

```env 
POSTGRES_DB=airport
POSTGRES_USER=airport
POSTGRES_PASSWORD=airport
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY="your-super-secret-key-here"
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```
Quick Start with Docker (Recommended)
Make sure you have Docker and Docker Compose installed on your machine.

Clone the repository:

Bash
git clone [https://github.com/T0p4ikUA/airport-api-service.git](https://github.com/T0p4ikUA/airport-api-service.git)
cd airport-api-service
Configure environment variables:

Bash
cp .env.sample .env
(Update .env with your secure values if needed)

Build and run containers:

Bash
docker-compose up --build -d
Run database migrations:

Bash
docker-compose exec app python manage.py migrate
Load initial sample data (Fixtures):

Bash
docker-compose exec app python manage.py loaddata fixture.json
Create a superuser (for Django Admin & testing):

Bash
docker-compose exec app python manage.py createsuperuser
API is up and running! Access it at: http://127.0.0.1:8000/

API Documentation (Swagger): http://127.0.0.1:8000/api/doc/swagger/

API Documentation (Redoc): http://127.0.0.1:8000/api/doc/redoc/

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
Set up your .env file and configure your local PostgreSQL database connection.

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
