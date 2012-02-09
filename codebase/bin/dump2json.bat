@echo off

REM ============================================================================
REM Set up environmental variables
REM ============================================================================
call environment.bat

REM ============================================================================
REM Clear the screen
REM ============================================================================
CLS

ECHO ###########################################################################
ECHO DUMP 2 JSON
ECHO ###########################################################################

REM ============================================================================
REM Confirm user has specified a database
REM ============================================================================
IF [%1] EQU [] GOTO USAGE

REM ============================================================================
REM Confirm user has specified an output file
REM ============================================================================
IF [%2] EQU [] GOTO USAGE

REM ============================================================================
REM Dump data from specified database to file
REM ============================================================================
:DUMPDATA
	SET APPLICATION_DB=%1
	SET DATAFILE=%2
	CD %APPLICATION_PYTHON%
	python manage.py dumpdata --indent=4 > %DATAFILE%
	CD %CURRENT%
	GOTO END

REM ============================================================================
REM Show command usage instructions
REM ============================================================================
:USAGE
    ECHO Database name and/or output file not specified. Exiting.
    ECHO Usage  : %0% DATABASE_NAME DATA_FILE
    ECHO Example: %0% myDatabase myData.json

REM ============================================================================
REM Finish
REM ============================================================================
:END
	ECHO Done.