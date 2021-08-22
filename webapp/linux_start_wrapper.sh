#!/bin/bash

echo "Starting up python app..."


export FLASK_APP=app_base
export FLASK_ENV=development


flask run &


echo "started. Exiting bash script"
