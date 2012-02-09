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
ECHO RUN DEBUG SERVER
ECHO ###########################################################################

REM ============================================================================
REM Confirm user has specified a database
REM ============================================================================
IF [%1] EQU [] GOTO USAGE

REM ============================================================================
REM Confirm user has specified a port
REM ============================================================================
IF [%2] EQU [] GOTO USAGE

REM ============================================================================
REM Run debug server for Django application
REM ============================================================================
:SHELL
	SET APPLICATION_DB=%1
	SET PORT=%2
	SET DJANGO_SETTINGS_MODULE=settings
	SET URLHOST=%HOSTNAME%:%PORT%
	SET TZ=GMT
	CD %APPLICATION_SRC%
	python manage.py runserver %URLHOST%
	CD %CURRENT%
	GOTO END

REM ============================================================================
REM Show command usage instructions
REM ============================================================================
:USAGE
    ECHO Database name and/or port number not specified. Exiting.
    ECHO Usage  : %0% DATABASE_NAME PORT
    ECHO Example: %0% myDatabase 8080

REM ============================================================================
REM Finish
REM ============================================================================
:END
	ECHO Done.