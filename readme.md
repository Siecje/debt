#Debt API

##Development Setup

```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create initial admin user
```shell
python manage.py createsuperuser
```

Run the API
```shell
python manage.py runserver
```

The API is now available at ```http://localhost:8000/api/v1.0/```

##Usage
Authentication

```shell
http --json POST http://localhost:8000/api/v1.0/auth/token \
username=username password=password
# Authenticated requests use 'Authorization: Token'
http --json GET http://localhost:8000/api/v1.0/credit-cards \
'Authorization:Token bb83e4b5f137958432aacde8c64c6e99e11b1'
```
