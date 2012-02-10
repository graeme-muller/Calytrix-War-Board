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
export WARBOARD_DB=$1
echo
echo Using database $WARBOARD_DB
echo

. ./environment.env

pushd $WARBOARD_SRC
python manage.py shell
popd
