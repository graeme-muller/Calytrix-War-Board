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
ECHO RESET / CLEAR DATABASE
ECHO ###########################################################################

REM ============================================================================
REM Confirm user has specified a database
REM ============================================================================
IF [%1] EQU [] GOTO USAGE

REM ============================================================================
REM Confirm user really wants to reset this database
REM ============================================================================
SET APPLICATION_DB=%1
set CONFIRM=
ECHO
ECHO WARNING: Database %APPLICATION_DB% will be completely
ECHO reset by this operation. Proceed?
:CONFIRMATION_LOOP
	SET /P CONFIRM=* [Y/N]?
	IF %CONFIRM% == Y GOTO SYNCDB
	IF %CONFIRM% == y GOTO SYNCDB
	IF %CONFIRM% == N GOTO ABORT
	IF %CONFIRM% == n GOTO ABORT
	GOTO CONFIRMATION_LOOP

REM ============================================================================
REM Reset database or abort operation as appropriaten
REM ============================================================================
:SYNCDB
	CD %APPLICATION_PYTHON%
	"%POSTGRES_BIN%\dropdb.exe" -U postgres %APPLICATION_DB%
	"%POSTGRES_BIN%\createdb.exe" -U postgres -E UTF8 %APPLICATION_DB%
	python manage.py syncdb --noinput
	CD %CURRENT%
	GOTO END

REM ============================================================================
REM Abort database reset operation
REM ============================================================================
:ABORT
	ECHO Operation cancelled.
	GOTO END

REM ============================================================================
REM Show command usage instructions
REM ============================================================================
:USAGE
    ECHO Database name not specified. Exiting.
    ECHO Usage  : %0% DATABASE_NAME
    ECHO Example: %0% myDatabase

REM ============================================================================
REM Finish
REM ============================================================================
:END
	ECHO Done.