![jeec-logo](resources/images/jeec_logo.png)
<p align="center">
  <img src="resources/images/brain.png">
</p>

### Table of contents
* [What is this?](#what-is-this)
* [Administration API](#administration-api)
* [CV Platform API](#cv-platform-api)
* [Website API](#website-api)
* [Tech Stack](#tech-stack)
* [Instructions to deploy locally](#instructions-to-deploy-locally)
* [Database Model](#database-model)
* [Running migrations](#running-migrations)
* [Authentication](#authentication)
* [Useful links](#useful-links)

## What is this?
Welcome to the **JEEC Brain**! This system serves the purpose of managing
all the technological services of the JEEC event.

It includes an Administration Dashboard were a user can access in order to **list/add/edit/delete** companies, speakers, activities, teams and colaborators.

The system consists of **3 main REST API's**
- **Administration API**
- **CV Platform API**
- **Website API**

## Administration API
This is were the requests to the administration endpoints are managed, which focuses on the creation, editing, deletion and listing of data related to the event.

**Companies**: 
- `list/add/edit/delete` companies;
- search companies;
- upload company **logo**;
- set **partnership levels** which include `main_sponsor/gold/silver/bronze`;

**Speakers**:
- `list/add/edit/delete` speakers;
- search speakers;
- upload speaker **image**;
- set **spotlight speakers** which will be instantly included in the homepage of the website

**Teams**:
- `list/add/edit/delete` teams;
- search teams;
- `list/add/edit/delete` team members;
- search team members;
- upload team member **image**;

**Activities**: (workshops, tech talks, panel discussions, presentations, job fair, matchmaking)
- `list/add/edit/delete` different types of activities;
- search activities (by type, name);

## CV Platform API
This endpoints serve the purpose of presenting the CV Submission Platform that the students and companies have access to. In resume, this includes Fenix Authentication handling, the company login page, file submission by the students, and file download by the companies.

## Website API
This endpoints are used to present data to the [JEEC website](https://www.jeec.ist). The website requests the companies, speakers, activities and teams data to this API.

Includes endpoints to:
- `GET` speakers
- `GET` activities
- `GET` companies
- `GET` teams

All the **endpoints support search parameters**, so for instance, a request can be made as:

`GET` `/website/speakers?spotlight=False`

and only the spotlight speakers will be requested. This **enables search queries** to the endpoints using different variables.

## Tech Stack
*   Python 3.6
*   Flask
*   PostgreSQL


## Instructions to deploy locally
1. Clone this repository;
2. Install PostreSQL;
3. Create virtual environment and install required dependencies with:
    - `python3.6 -m virtualenv venv`
    - `source venv/bin/activate`
    - `python3.6 -m pip install -r requirements.txt`
4. Run the database service with:
    - `sudo service postgresql start`
5. Create a database in postgresql for the application:
    - `psql postgres`
    - `CREATE DATABASE jeec_brain;`
6. Insert the .env file in the root of the project and fill in the missing variables:
    ```
        SECRET_KEY=
        APP_ENV=<[development|testing|staging|production]>
        FLASK_DEBUG="True"

        # Database (update APP_DB with the name of your database)
        APP_DB = 
        DATABASE_URL = "postgresql:///"

        # File submission
        CV_SUBMISSION_OPEN = "FALSE"
        UPLOAD_FOLDER = '/jeec_brain/storage/'
        
        # Credentials required to access the Website API
        CLIENT_USERNAME = 
        CLIENT_KEY = 
    ```
8. Migrate the database with:
    - `python manage.py db init`
    - `python manage.py db migrate`
    - `python manage.py db upgrade`
9. Deploy the Flask application with:
    - `python manage.py runserver`


The application runs on port **8081**.


## Database Model
![er-model](resources/images/ER.png)


## Running migrations
1. Data migrations are ran using the commands:
    - `python manage.py db migrate`
    - `python manage.py db upgrade`


## Authentication

The **Administration API** and the **CV_Platform API** use session Authentication, implemented by *flask_login* library and cache. 
**Users must be created in the database**, and then provide their username and password to acess the system.

- **Roles:**
Each user has a role in the system. For instance, if your are an `admin` you will have permission to do everything in the administration pages (add/edit/delete/list data). **But other roles, can be used to restrict the user actions**. The role `company-admin`, for example, will be able to see all the data, but only add and edit companies. 

This role's feature is very useful if you want to spread the usage of the platform throughout the team, without everyone being able to mess with the valuable data.

When it comes to **Website API**, the autentication used is **BasicAuth**. So, we set the credentials in the .env file, and the website must provide this credentials in the headers of the requests, in order to get authenticated and be able to access the data.

### Useful links
* Flask Documentation - http://flask.pocoo.org/docs/1.0/
* The most complete Flask Tutorial ever - https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
