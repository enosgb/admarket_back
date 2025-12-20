# AdMarket API

API for listing and manage Ads

- [ ] Authentication 
  - [ ] Login
  - [ ] Logout
  - [ ] Reset password
  - [ ] Forgot password
- [ ] Users management
- [ ] Categories management
- [ ] Products management
- [ ] Store management
- [ ] Ads management
- [ ] Marketplace
- [ ] Features
  - [ ] Filters and Sorting
  - [ ] Favorites
  - [ ] Delay - Front End Loading
- [ ] Optimization
  - [ ] Pagination
  - [ ] Cache
- [ ] Tests

## Clone project
```bash
git clone https://github.com/enosgb/admarket_back
```
## Navigate to the project folder
```bash
cd admarket_back
```

## Requirements
- Python 3.12
- django v6.0
- psycopg2-binary v2.9.11
- black v25.12.0
- ruff v0.14.10
- djangorestframework v3.16.1
- drf-yasg v1.21.11

## Database - Docker PostgreSQL
```bash
docker compose up -d
```

## How to run

Create env
```bash
python3.12 -m venv venv
```
Activate env - Linux 
```bash
source venv/bin/activate 
```
or

Activate env - Windows
```bash
source venv/Scripts/Activate 
```
Install requirements
```bash
pip install -r requirements.txt
```

Run migrations
```bash
python manage.py migrate
```
Run server
```bash
python manage.py runserver
```
