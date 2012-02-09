#!/bin/bash

clear

# ============================================================================
# Confirm user has specified a database
# ============================================================================
if [ -z $1 ]
then
    echo Database name not specified. Exiting.
    echo Usage  : $0 DATABASE_NAME
    echo Example: $0 myDatabase
    exit
fi

# ============================================================================
# Provide shell prompt for Django application
# ============================================================================
export APPLICATION_DB=$1
echo
echo Using database $APPLICATION_DB
echo

. ./APPLICATION.env

pushd $APPLICATION_HOME
python manage.py shell
popd
