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
ECHO LOAD DATA
ECHO ###########################################################################

REM ============================================================================
REM Confirm user has specified a database
REM ============================================================================
IF [%1] EQU [] GOTO USAGE

REM ============================================================================
REM Confirm user has specified a source file
REM ============================================================================
IF [%2] EQU [] GOTO USAGE

REM ============================================================================
REM Confirm user really wants to load data into this database
REM ============================================================================
SET APPLICATION_DB=%1
SET DATAFILE=%2
set CONFIRM=
ECHO
ECHO Please confirm that you wish to load data into database %APPLICATION_DB%
:CONFIRMATION_LOOP
	SET /P CONFIRM=* [Y/N]?
	IF %CONFIRM% == Y GOTO LOADDATA
	IF %CONFIRM% == y GOTO LOADDATA
	IF %CONFIRM% == N GOTO ABORT
	IF %CONFIRM% == n GOTO ABORT
	GOTO CONFIRMATION_LOOP

REM ============================================================================
REM Load data into database
REM ============================================================================
:LOADDATA
	CD %APPLICATION_PYTHON%
	python manage.py loaddata %DATAFILE%
	CD %CURRENT%
	GOTO END

REM ============================================================================
REM Abort load data into database operation
REM ============================================================================
:ABORT
	ECHO Operation cancelled.
	GOTO END

REM ============================================================================
REM Show command usage instructions
REM ============================================================================
:USAGE
    ECHO Database name and/or source file not specified. Exiting.
    ECHO Usage  : %0% DATABASE_NAME DATA_FILE
    ECHO Example: %0% myDatabase myData.json

REM ============================================================================
REM Finish
REM ============================================================================
:END
	ECHO Done.