# Airport API Service

API service for airport and flight management written on Django REST Framework (DRF).

## Installing using GitHub

1. Clone the repository:
   ```bash
   git clone [https://github.com/T0p4ikUA/airport-api-service.git](https://github.com/T0p4ikUA/airport-api-service.git)
   cd airport-api-service
Create and activate virtual environment:

Bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt

Run migrations:

Bash
python manage.py migrate
Create a superuser (for admin panel):

Bash
python manage.py createsuperuser
Run the server:

Bash
python manage.py runserver