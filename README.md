# Assessment fastAPI


## Introduction

This application was developed as an assessment of fastAPI.

## Activating the virtual environment and installing dependencies

This project uses [Poetry](https://python-poetry.org/) to handle the virtual environment.
I assume you have installed `Poetry` at this point.

First, install the dependencies:

    poetry install --no-root

The remainder of the instruction assume the virtual environment created by Poetry has been activated.
One way of doing that is this way:

    poetry shell

## Usage instructions

The file `config.yml` contains the configuration. For now, it only contains the configuration
of the database. Update this according to your requirements.

To apply the migration scripts to the configured database, run this command:

    python -m songs_api.apply_migrations

Start in development mode:

    fastapi dev songs_api/main.py

Start in production mode:

    fastapi songs_api/main.py

## Deployment with docker

A `Dockerfile` is provided to build a docker image for the songs API. Run this command to build the image:

    docker build . -t songs:latest

A `docker-compose.yml` file is provided that starts up a PostgreSQL database, the FastAPI application and NGINX.
Start the docker containers with this command:

    docker compose up

The first time the application is run with docker compose, the PostgreSQL database will apply all mgirations scripts
from the directory `migrations`.

## Example interaction with the API

Below is an example interation with the API generated with Pycharm's support to execute HTTP requests:

```
POST http://127.0.0.1:8000/songs
Content-Type: application/json

{
    "title": "The Day After Eunice",
    "composer": "Sander Kooijmans",
    "artist": "Sander Kooijmans",
    "year_of_release": 2025
}


HTTP/1.1 201 Created
date: Wed, 07 May 2025 12:11:02 GMT
server: uvicorn
content-length: 120
content-type: application/json

{
  "title": "The Day After Eunice",
  "composer": "Sander Kooijmans",
  "artist": "Sander Kooijmans",
  "year_of_release": 2025,
  "id": 1
}


POST http://127.0.0.1:8000/songs
Content-Type: application/json

{
    "title": "The Day After Eunice",
    "composer": "Sander Kooijmans",
    "artist": "Sander Kooijmans",
    "year_of_release": 2025
}


HTTP/1.1 201 Created
date: Wed, 07 May 2025 12:11:18 GMT
server: uvicorn
content-length: 114
content-type: application/json

{
  "title": "Brit On A Buoy",
  "composer": "Sander Kooijmans",
  "artist": "Sander Kooijmans",
  "year_of_release": 2024,
  "id": 2
}


GET http://127.0.0.1:8000/songs

HTTP/1.1 200 OK
date: Wed, 07 May 2025 12:11:38 GMT
server: uvicorn
content-length: 237
content-type: application/json

[
  {
    "title": "The Day After Eunice",
    "composer": "Sander Kooijmans",
    "artist": "Sander Kooijmans",
    "year_of_release": 2025,
    "id": 1
  },
  {
    "title": "Brit On A Buoy",
    "composer": "Sander Kooijmans",
    "artist": "Sander Kooijmans",
    "year_of_release": 2024,
    "id": 2
  }
]
```
