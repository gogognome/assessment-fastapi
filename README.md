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
