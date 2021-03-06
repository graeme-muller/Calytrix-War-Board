#!/bin/bash
clear
# ============================================================================
# Confirm user has specified a database
# ============================================================================
if [ -z $1 ]
then
	echo Database name not specified. Exiting.
	echo Usage  : $0 APPLICATION_DATABASE
	echo Example: $0 myDatabase
	exit
fi
# ============================================================================
# Confirm user really wants to reset this database
# ============================================================================
export WARBOARD_DB=$1
export CONFIRM=x
until [ "$CONFIRM" == "Y" ] || [ "$CONFIRM" == "y" ] || [ "$CONFIRM" == "N" ] || [ "$CONFIRM" == "n" ]
do
	echo
	echo WARNING: Database $WARBOARD_DB will be completely
	echo reset by this operation. Proceed?
	echo [Y/N]?
	read CONFIRM
done
# ============================================================================
# Reset database or abort operation as appropriate
# ============================================================================
if [ "$CONFIRM" == "Y" ] || [ "$CONFIRM" == "y" ]
then
	. ./environment.env
	dropdb -U postgres $WARBOARD_DB
	createdb -U postgres $WARBOARD_DB
	pushd $WARBOARD_SRC
	python manage.py syncdb --noinput
	popd
else
	echo Operation cancelled.
fi
