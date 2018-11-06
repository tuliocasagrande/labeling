Labeling
========

## Installing

This app currently uses Python 2. Use of virtualenv is recommended:

1. Install virtualenv:
```
pip install virtualenv
```

2. Create virtual environment:
```
virtualenv --python=python2 venv
```

3. Activate the virtual environment (you're going to need this to every terminal):
```
source venv/bin/activate
```

4. Install app libraries:
```
pip install -r requirements.txt
```

5. Configure the following environment variables:
```
LB_SECRET_KEY
LB_DATABASE_URL
LB_SENDGRID_USR
LB_SENDGRID_PWD
LB_ADMIN_MAIL
```

6. Install PostgreSQL (https://www.postgresql.org) and create a database called `labeling`:
```
sudo -u postgres psql      # might be different depending on you OS
create database labeling;  # don't forget the semicolon
\l                         # in case you want to check the database was created
\q                         # quit
```

7. Apply migrations:
```
python manage.py migrate
```

## Running

```
python manage.py runserver
```
