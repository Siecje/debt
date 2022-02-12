# Debt API

## Features

- Models
  - [x]Incomes
  - [x]Expenses
  - [x]Credit Cards
  - [x]Overdrafts
  - [ ]Loans
  - [x]Investments
  - [x]Tax Brackets
- [x]Calculate which debt to pay off
- [x]Calculate time till debt free
- [ ]Visualize net worth with money in different accounts

## Development Setup

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/developement.txt
```

```shell
python manage.py migrate
```

```shell
# Run the API
python manage.py runserver
```

The API is now available at [http://localhost:8000/api/v1.0/](http://localhost:8000/api/v1.0/)

## Usage

### Create User

```shell
http --json POST http://localhost:8000/api/v1.0/users \
username=username password=password email=username@example.com
```

### Authentication

```shell
http --json POST http://localhost:8000/api/v1.0/auth/token \
username=username password=password
```

```shell
HTTP/1.0 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Date: Thu, 18 Jun 2015 17:27:23 GMT
Server: WSGIServer/0.1 Python/2.7.6
X-Frame-Options: SAMEORIGIN

{
    "token": "ae25e52afb6d929bdcca7f413d26043b5ae5348d"
}
```

### Get Data

```shell
$ TOKEN=ae25e52afb6d929bdcca7f413d26043b5ae5348d
# Authenticated requests use 'Authorization: Token'
$ http --json GET http://localhost:8000/api/v1.0/credit-cards \
"Authorization:Token "$TOKEN""
```

## Tests

```shell
coverage run --source='.' manage.py test
coverage html
firefox tmp/coverage/index.html
```
