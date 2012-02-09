#!/bin/bash
clear
# ============================================================================
# Confirm user has specified a database
# ============================================================================
if [ -z $1 ]
then
        echo Database name not specified. Exiting.
        echo Usage  : $0 DATABASE_NAME DATA_FILE
        echo Example: $0 myDatabase myData.json
        exit
fi
# ============================================================================
# Confirm user has specified a source file
# ============================================================================
if [ -z $2 ]
then
        echo Data file not specified. Exiting.
        echo Usage  : $0 DATABASE_NAME DATA_FILE
        echo Example: $0 myDatabase myData.json
        exit
fi
# ============================================================================
# Confirm user really wants to load data into this database
# ============================================================================
export APPLICATION_DB=$1
export DATAFILE=$2
export CONFIRM=x
until [ "$CONFIRM" == "Y" ] || [ "$CONFIRM" == "y" ] || [ "$CONFIRM" == "N" ] || [ "$CONFIRM" == "n" ]
do
        echo
        echo Please confirm that you wish to load data into database $APPLICATION_DB
        echo [Y/N]?
        read CONFIRM
done
# ============================================================================
# Load data into database or abort operation as appropriate
# ============================================================================
if [ "$CONFIRM" == "Y" ] || [ "$CONFIRM" == "y" ]
then
	. ./environment.env
	pushd $INJECTPLANNER_SRC
	python manage.py loaddata $DATAFILE
	popd
else
        echo Operation cancelled.
fi
