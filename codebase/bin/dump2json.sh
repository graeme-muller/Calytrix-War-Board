#!/bin/bash
clear
# ============================================================================
# Confirm user has specified a database
# ============================================================================
if [ -z $1 ]
then
        echo Database name not specified. Exiting.
        echo Usage  : $0 DATABASE_NAME OUTPUT_FILE
        echo Example: $0 myDatabase outputFile.json
        exit
fi
export APPLICATION_DB=$1
# ============================================================================
# Confirm user has specified an output file
# ============================================================================
if [ -z $2 ]
then
        echo Output file not specified. Exiting.
        echo Usage  : $0 DATABASE_NAME OUTPUT_FILE
        echo Example: $0 myDatabase outputFile.json
        exit
fi
export OUTPUTFILE=$2
#============================================================================
# Dump data from specified database to file
# ============================================================================
. ./environment.env
pushd $INJECTPLANNER_SRC
python manage.py dumpdata --indent=4 > $OUTPUTFILE
popd
