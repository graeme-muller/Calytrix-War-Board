@echo off

REM --------------------------------------------------
REM Modify these settings to suit your environment
REM --------------------------------------------------
set HOSTNAME=%COMPUTERNAME%
set PORT=8000
set POSTGRES_BIN=c:\progra~1\PostgreSQL\9.0\bin
set PYTHON_BIN=c:\dev\python\32bit\2.6

REM --------------------------------------------------

REM --------------------------------------------------
REM These settings should not need changing
REM --------------------------------------------------
set PATH=%PATH%;%PYTHON_BIN%;%POSTGRES_BIN%

REM The %~dp0 used below is a special environmental
REM variable which contains the absolute path of the
REM currently executing batch file (i.e. the file
REM you are looking at right now)

set CURRENT=%~dp0
set WORKSPACE=%CURRENT%..\src

set APPLICATION_ROOT=%WORKSPACE%
set PYTHON_SRC=%WORKSPACE%\python
set APPLICATION_SRC=%PYTHON_SRC%\applications
set DJANGO_HOME=%PYTHON_SRC%\external\django\1.3

set PYTHONPATH=%DJANGO_HOME%;%APPLICATION_PYTHON%
set DJANGO_SETTINGS_MODULE=settings

set TZ=GMT
REM --------------------------------------------------