# Ad Market API

API for listing and manage ads

## Requirements
django
psycopg2-binary

## Database
```bash
docker compose up -d
```

## How to run

```bash
python3.12 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

```