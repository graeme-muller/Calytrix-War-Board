#!/bin/bash

clear

# ============================================================================
# Confirm user has specified a database
# ============================================================================
if [ -z $1 ]
then
    echo Database name not specified. Exiting.
    echo Usage  : $0 DATABASE_NAME PORT
    echo Example: $0 myDatabase 8888
    exit
fi

# ============================================================================
# Confirm user has specified a port
# ============================================================================
if [ -z $2 ]
then
    echo Port number not specified. Exiting.
    echo Usage  : $0 DATABASE_NAME PORT
    echo Example: $0 myDatabase 8888
    exit
fi

# ============================================================================
# Run debug server for Django application
# ============================================================================
export APPLICATION_DB=$1
export PORT=$2
echo
echo Using database $APPLICATION_DB
echo

. ./APPLICATION.env

export DJANGO_SETTINGS_MODULE=settings
export URLHOST=$HOSTNAME:$PORT
export TZ=GMT

pushd $APPLICATION_HOME
python manage.py runserver $URLHOST
popd
