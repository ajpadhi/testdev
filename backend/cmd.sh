#!/bin/bash

if [ $1 == "format" ]
then
    poetry run autoflake app
    poetry run isort app
    poetry run black app
    poetry run flake8 app
    poetry run mypy app
elif [ $1 == "test" ]
then
    export CI=true && poetry run coverage run --source ./app -m pytest --disable-warnings
    poetry run coverage xml
    poetry run coverage html
    poetry run coverage report -m
elif [ $1 == "start" ]
then
    poetry run python -m app.main
else
   echo "unknown command $1"
fi
