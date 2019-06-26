# JEEC CV Platform 

### Table of contents
* [What is this?](#what-is-this)
* [Tech Stack](#tech-stack)
* [Instructions to deploy locally](#instructions-to-deploy-locally)
* [Production Environment](#production-environment)
* [Useful links](#useful-links)

## What is this?
Welcome to the JEEC CV Platform! This service is open during the event so that students can submit their resume's to the companies that attended. 

## Tech Stack and key concepts
*   Python
*   Flask
*   PostgreSQL


## Instruction to deploy locally
1. Fork this repository
2. Install PostreSQL
2. Install required dependencies inside the /webapp directory with:
    - `pip install -r requirement.txt`
3. Run the database service with:
    - `sudo service postgresql start`
4. Create a database in postgresql for the application
5. Ask JEEC previous developers the .env file
    - Update the APP_DB name in the .env
6. Migrate the database with:
    - `python manage.py db init`
    - `python manage.py db migrate`
    - `python manage.py bg upgrade`
7. Deploy the Flask application with:
    - `flask run`


### Useful links
* Flask Documentation - http://flask.pocoo.org/docs/1.0/
* The most complete Flask Tutorial ever - https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world


