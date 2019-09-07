# JEEC Administration System 

### Table of contents
* [What is this?](#what-is-this)
* [Tech Stack](#tech-stack)
* [Instructions to deploy locally](#instructions-to-deploy-locally)
* [Production Environment](#production-environment)
* [Useful links](#useful-links)

## What is this?
Welcome to the JEEC Brain! This system serves the purpose of managing
all the technological services of the JEEC event. 

## Tech Stack and key concepts
*   Python 3.6
*   Flask
*   PostgreSQL


## Instruction to deploy locally
1. Clone this repository;
2. Install PostreSQL;
2. Create virtual environment and install required dependencies with:
    - `python3.6 -m virtualenv venv`
    - `python3.6 -m pip install -r requirement.txt`
3. Run the database service with:
    - `sudo service postgresql start`
4. Create a database in postgresql for the application:
    - `psql postgres`
    - `CREATE DATABASE jeec_brain;`
5. Ask JEEC previous developers the .env file;
6. Update the **APP_DB** name in the .env, with the name of your database;
6. Migrate the database with:
    - `python manage.py db init`
    - `python manage.py db migrate`
    - `python manage.py db upgrade`
7. Deploy the Flask application with:
    - `python manage runserver`


The application runs on port **8081**.


## Database Model (to be added)


## Running migrations
Data migrations are ran using the commands:
    - `python manage.py db migrate`
    - `python manage.py db upgrade`


### Useful links
* Flask Documentation - http://flask.pocoo.org/docs/1.0/
* The most complete Flask Tutorial ever - https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world


