#!/bin/bash

if [ -v "$DEBUG" ]; then
    set -e
    echo 'DEBUG SCRIPT'
    ./PyRestPdf/manage.py migrate --noinput
    ./PyRestPdf/manage.py loaddata debug_data.json
    ./PyRestPdf/manage.py runserver 0.0.0.0:8000
else
    echo 'PROD SCRIPT'
    ./PyRestPdf/manage.py migrate --noinput
fi
