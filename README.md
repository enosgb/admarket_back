# AdMarket API

API for listing and manage Ads

- [x] Authentication 
  - [x] Login
  - [x] Logout
  - [x] Email util
  - [x] Reset password
  - [x] Change password
  - [x] Testes
- [ ] Users management
  - [x] CRUD
  - [x] Filters and Sorting  
  - [x] Tests
  - [ ] Cache
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
  - [x] Pagination
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
- asgiref==3.11.0
- black==25.12.0
- certifi==2025.11.12
- charset-normalizer==3.4.4
- click==8.3.1
- cloudinary==1.44.1
- Django==6.0
- django-cloudinary-storage==0.3.0
- django-filter==25.2
- djangorestframework==3.16.1
- drf-yasg==1.21.11
- idna==3.11
- inflection==0.5.1
- iniconfig==2.3.0
- mypy_extensions==1.1.0
- packaging==25.0
- pathspec==0.12.1
- pillow==12.0.0
- platformdirs==4.5.1
- pluggy==1.6.0
- psycopg2-binary==2.9.11
- Pygments==2.19.2
- pytest==9.0.2
- pytest-django==4.11.1
- pytest-mock==3.15.1
- python-dotenv==1.2.1
- pytokens==0.3.0
- pytz==2025.2
- PyYAML==6.0.3
- requests==2.32.5
- ruff==0.14.10
- six==1.17.0
- sqlparse==0.5.5
- uritemplate==4.2.0
- urllib3==2.6.2


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
