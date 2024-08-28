# Event Manager

## General description of the service
- Users must be able to register an account

- Users must be able to log in into their account

- A system of token rotation must be implemented. For this the API needs to provide a user with access_token and a refresh_token, as well as a way to refresh and validate the access_token. The lifetime of the access_token should be 1 hour and the lifetime of the refresh_token 1 day

- Users must be able to create events in the app's database (slqlite)

- Users must be able to see the list of events they have created

- Users must be able to see a list of all events

- Users must be able to edit the events they have created but not the ones created by other users

- Users must be able to register to an event or un-register. This can only be done in future events and not in past events.

## Language, framework, orm

language - python3.11
framework - Django Rest Framework 3.15.2


## Run
````
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

python3 manage.py migrate
python3 manage.py runserver
```
````

## Test
```
python3 manage.py test 
```

## Swagger
http://127.0.0.1:8000/swagger/
