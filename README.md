# README #

## Summary ##

This repository is created by Volodymyr Vintila for test

## How to setup local development environment

### Preparations ###

* install packages from requirements.txt file
```
pip install -r requrements.txt
```

* create new file `{PROJECT_ROOT}/.env` and copy into it the content of `{PROJECT_ROOT}/env.example`

These file contains the environment vars which are used in the project code and for create docker container.

### Setup Postgres Using Docker Image

For running docker containers ensure that you have installed docker-engine and docker-cli. Documentation for 
installing docker can be found [here](https://docs.docker.com/engine/install/) 

#### For debian based linux repositories:

For running docker container execute next command

Be careful, use variables specified in .env

Run docker container

```
sudo docker run -d -p 55005:5432 --name mycontainer -e POSTGRES_PASSWORD=mypassword postgres
```
Open container bash

```
sudo docker exec -it mycontainer bash
```

For using PostgreSQL, you will need to switch to that user account with the command:

```
su - postgres
```
You will then be able to log into the PosgreSQL client with the command:
```
psql
```

Init PostgreSQL DB following [this instructions](https://github.com/Volodyan08/github_study/blob/main/postgers/setup_postgres.md)

### Apply migrations

Create a migration repository:
```
flask db init
```
Generate an initial migration:
```
flask migrate
```
Apply the changes described by the migration script to your database:
```
flask upgrate
```

### Now your flask application is ready to use


```
flask run
```

## Import user data

Python module which upload user data from `.csv` file to database. Make sure, that column name similar to
`first name`, `last name`, `Email`.

For upload data from `.csv` file use next command: 

```
python import_user_data.py
```

Then input path to `.csv` file in command line. And that's all. 

## Sync data from nimble /contacts endpoint

Python module which obtain user data from specified endpoint and save into database.

For upload data from nimble endpoint use next command: 

```
python import_user_data.py
```
For make script executable regularly you can use cron. Cron is a time-based job scheduler in Unix-like operating 
systems, including Linux and macOS. 