#!/bin/bash

if [ -v "$DEBUG" ]; then
    set -e
    echo 'DEBUG SCRIPT'
    ./manage.py migrate --noinput
    ./manage.py loaddata debug_data.json
    ./manage.py runserver 0.0.0.0:8000
else
    echo 'PROD SCRIPT'
    ./manage.py migrate --noinput
fi
