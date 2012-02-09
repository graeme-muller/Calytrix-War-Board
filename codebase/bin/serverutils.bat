@echo off

REM --------------------------------------------------
REM Modify these settings to suit your environment
REM --------------------------------------------------
set HOSTNAME=%COMPUTERNAME%
set PORT=8301
set POSTGRES_BIN=%PROGRAMFILES%\PostgreSQL\9.0\bin
set PYTHON_BIN=c:\dev\python\32bit\2.7

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
set PYTHONPATH=%DJANGO_HOME%;%APPLICATION_SRC%
set DJANGO_SETTINGS_MODULE=settings
set TZ=GMT
REM --------------------------------------------------

REM --------------------------------------------------
REM Modify the items below if you need to add more
REM menu options and/or databases
REM --------------------------------------------------
:DO_MENU
	echo %APPLICATION_SRC%
	echo *---------------------------------------------------------*
	echo "                                                         "
	echo *                Django Server Utilities                  *
	echo "                 on: %HOSTNAME%:%PORT%                   "
	echo "                                                         "
	echo * Select Operation:                                       *
	echo *---------------------------------------------------------*
	echo * [r#]   Run server with # DB
	echo * [s#]   Sync DB to      # DB
	echo * [c#]   Clear           # DB (Start Fresh)
	echo * [sr#]  Sync, then run server with # DB
	echo * [cr#]  Clear, then run server with # DB
	echo * [cmd#] Open a # shell
	echo * [demodata#] fill DB # with demo data
	echo * [dd# filename] dumpdata for # DB
	echo * [ld# filename] loaddata for # DB
	echo * [test]  Run Test Suite
	echo *
	echo * # = 1: WARBOARD
	echo * # = 2: not in use
	echo * # = 3: not in use
	echo * # = 4: not in use
	echo * # = 5: Testing / Sandbox Area
	echo *
	echo * [x] Quit without any further action
	echo *----------------------------------
	set ITEM=
	SET /P ITEM=* Please choose an option from the above list:
	echo *
	IF %ITEM% == s1 GOTO sDB_A
	IF %ITEM% == r1 GOTO rDB_A
	IF %ITEM% == c1 GOTO cDB_A
	IF %ITEM% == sr1 GOTO srDB_A
	IF %ITEM% == cr1 GOTO crDB_A
	IF %ITEM% == cmd1 GOTO cmdDB_A
	IF %ITEM% == dd1 GOTO ddDB_A
	IF %ITEM% == ld1 GOTO ldDB_A
	IF %ITEM% == s2 GOTO sDB_B
	IF %ITEM% == r2 GOTO rDB_B
	IF %ITEM% == c2 GOTO cDB_B
	IF %ITEM% == sr2 GOTO srDB_B
	IF %ITEM% == cr2 GOTO crDB_B
	IF %ITEM% == cmd2 GOTO cmdDB_B
	IF %ITEM% == dd2 GOTO ddDB_B
	IF %ITEM% == ld2 GOTO ldDB_B
	IF %ITEM% == s3 GOTO sDB_C
	IF %ITEM% == r3 GOTO rDB_C
	IF %ITEM% == c3 GOTO cDB_C
	IF %ITEM% == sr3 GOTO srDB_C
	IF %ITEM% == cr3 GOTO crDB_C
	IF %ITEM% == cmd3 GOTO cmdDB_C
	IF %ITEM% == dd3 GOTO ddDB_C
	IF %ITEM% == ld3 GOTO ldDB_C
	IF %ITEM% == s4 GOTO sDB_D
	IF %ITEM% == r4 GOTO rDB_D
	IF %ITEM% == c4 GOTO cDB_D
	IF %ITEM% == sr4 GOTO srDB_D
	IF %ITEM% == cr4 GOTO crDB_D
	IF %ITEM% == cmd4 GOTO cmdDB_D
	IF %ITEM% == dd4 GOTO ddDB_D
	IF %ITEM% == ld4 GOTO ldDB_D
	IF %ITEM% == s5 GOTO sDB_E
	IF %ITEM% == r5 GOTO rDB_E
	IF %ITEM% == c5 GOTO cDB_E
	IF %ITEM% == sr5 GOTO srDB_E
	IF %ITEM% == cr5 GOTO crDB_E
	IF %ITEM% == cmd5 GOTO cmdDB_E
	IF %ITEM% == dd5 GOTO ddDB_E
	IF %ITEM% == ld5 GOTO ldDB_E
	IF %ITEM% == test GOTO RUN_TEST_SUITE
	IF %ITEM% == x GOTO QUIT
	GOTO INVALID_CHOICE

:INVALID_CHOICE
	echo *
	echo * '%ITEM%' is an Invalid selection.
	echo *
	GOTO DO_MENU

:DB_A
	set APPLICATION_DB=warboard_db
	set APPLICATION_DBFILE=%APPLICATION_DB%
	GOTO OPERATIONS

:DB_B
	set APPLICATION_DB=delete_me
	set APPLICATION_DBFILE=%APPLICATION_DB%
	GOTO OPERATIONS

:DB_C
	set APPLICATION_DB=delete_me
	set APPLICATION_DBFILE=%APPLICATION_DB%
	GOTO OPERATIONS

:DB_D
	set APPLICATION_DB=delete_me
	set APPLICATION_DBFILE=%APPLICATION_DB%
	GOTO OPERATIONS

:DB_E
	set APPLICATION_DB=application_sandbox
	set APPLICATION_DBFILE=%APPLICATION_DB%
	GOTO OPERATIONS

REM ------------------- START DB operations
REM ------------------- DB_A operations
:sDB_A
	set OP=SYNC
	GOTO DB_A
:rDB_A
	set OP=RUNSERVER
	GOTO DB_A
:cDB_A
	set OP=CLEAR
	GOTO DB_A
:srDB_A
	set OP=SYNCRUNSERVER
	GOTO DB_A
:crDB_A
	set OP=CLEARRUNSERVER
	GOTO DB_A
:cmdDB_A
	set OP=SHELL
	GOTO DB_A
:ddDB_A
	set OP=DUMPDATA
	GOTO DB_A
:ldDB_A
	set OP=LOADDATA
	GOTO DB_A
REM ------------------- DB_B operations
:sDB_B
	set OP=SYNC
	GOTO DB_B
:rDB_B
	set OP=RUNSERVER
	GOTO DB_B
:cDB_B
	set OP=CLEAR
	GOTO DB_B
:srDB_B
	set OP=SYNCRUNSERVER
	GOTO DB_B
:crDB_B
	set OP=CLEARRUNSERVER
	GOTO DB_B
:cmdDB_B
	set OP=SHELL
	GOTO DB_B
:ddDB_B
	set OP=DUMPDATA
	GOTO DB_B
:ldDB_B
	set OP=LOADDATA
	GOTO DB_B
REM ------------------- DB_C operations
:sDB_C
	set OP=SYNC
	GOTO DB_C
:rDB_C
	set OP=RUNSERVER
	GOTO DB_C
:cDB_C
	set OP=CLEAR
	GOTO DB_C
:srDB_C
	set OP=SYNCRUNSERVER
	GOTO DB_C
:crDB_C
	set OP=CLEARRUNSERVER
	GOTO DB_C
:cmdDB_C
	set OP=SHELL
	GOTO DB_C
:ddDB_C
	set OP=DUMPDATA
	GOTO DB_C
:ldDB_C
	set OP=LOADDATA
	GOTO DB_C
REM ------------------- DB_D operations
:sDB_D
	set OP=SYNC
	GOTO DB_D
:rDB_D
	set OP=RUNSERVER
	GOTO DB_D
:cDB_D
	set OP=CLEAR
	GOTO DB_D
:srDB_D
	set OP=SYNCRUNSERVER
	GOTO DB_D
:crDB_D
	set OP=CLEARRUNSERVER
	GOTO DB_D
:cmdDB_D
	set OP=SHELL
	GOTO DB_D
:ddDB_D
	set OP=DUMPDATA
	GOTO DB_D
:ldDB_D
	set OP=LOADDATA
	GOTO DB_D
REM ------------------- DB_E operations
:sDB_E
	set OP=SYNC
	GOTO DB_E
:rDB_E
	set OP=RUNSERVER
	GOTO DB_E
:cDB_E
	set OP=CLEAR
	GOTO DB_E
:srDB_E
	set OP=SYNCRUNSERVER
	GOTO DB_E
:crDB_E
	set OP=CLEARRUNSERVER
	GOTO DB_E
:cmdDB_E
	set OP=SHELL
	GOTO DB_E
:ddDB_E
	set OP=DUMPDATA
	GOTO DB_E
:ldDB_E
	set OP=LOADDATA
	GOTO DB_E
REM ------------------- END DB operations





REM -----------------------------------------------------------------------------------------------
REM -----------------------------------------------------------------------------------------------
REM 		IT SHOULD NOT BE NECESSARY TO
REM 		    MODIFY BELOW THIS LINE
REM -----------------------------------------------------------------------------------------------
REM -----------------------------------------------------------------------------------------------
:OPERATIONS
	if %OP% == SYNC GOTO SYNCH_DB
	if %OP% == SYNCRUNSERVER GOTO SYNCH_DB
	if %OP% == CLEAR GOTO CLEAR_DB
	if %OP% == CLEARRUNSERVER GOTO CLEAR_DB
	if %OP% == RUNSERVER GOTO RUN_SERVER
	if %OP% == SHELL GOTO RUN_SHELL
	if %OP% == DUMPDATA GOTO DUMP_DATA
	if %OP% == LOADDATA GOTO LOAD_DATA
	GOTO INVALID_CHOICE

:CLEAR_DB
	echo *
	echo * Emptying Database %APPLICATION_DB%...
	echo *
	"%POSTGRES_BIN%\dropdb.exe" -U postgres %APPLICATION_DB%
	"%POSTGRES_BIN%\createdb.exe" -U postgres -E UTF8 %APPLICATION_DB%
	GOTO APPLICATION_APP_SYNCH

:DUMP_DATA
	SET /P DD_FILENAME=* Please enter full path and filename for data:
	echo *
	echo * Dumping Database %APPLICATION_DB% to "%DD_FILENAME%"...
	echo *
	cd %APPLICATION_SRC%
	python manage.py dumpdata --indent=4 > "%DD_FILENAME%"
	echo * Done.
	echo *
	GOTO DO_MORE

:LOAD_DATA
	SET /P DD_FILENAME=* Please enter full path and filename for JSON data:
	echo *
	echo * Loading data from %DD_FILENAME% into Database %APPLICATION_DB%
	echo *
	cd %APPLICATION_SRC%
	python manage.py loaddata "%DD_FILENAME%"
	echo * Data loaded.
	echo *
	GOTO DO_MORE

:SYNCH_DB
	echo *
	echo * Synchronising Database to %APPLICATION_DBFILE%...
	echo *
	"%POSTGRES_BIN%\dropdb.exe" -U postgres %APPLICATION_DB%
	"%POSTGRES_BIN%\createdb.exe" -U postgres -E UTF8 %APPLICATION_DB%
	GOTO APPLICATION_APP_SYNCH

:APPLICATION_APP_SYNCH
	cd %APPLICATION_SRC%
	python manage.py syncdb --noinput
	REM python manage.py loaddata main/fixtures/main.json
	if %OP% == SYNCRUNSERVER GOTO RUN_SERVER
	if %OP% == CLEARRUNSERVER GOTO RUN_SERVER
	GOTO DO_MORE

:RUN_SERVER
	cd %APPLICATION_SRC%
	start python manage.py runserver %HOSTNAME%:%PORT%
	GOTO DO_MORE

:RUN_SHELL
	cd %APPLICATION_SRC%
	python manage.py shell
	GOTO DO_MORE

:RUN_TEST_SUITE
	set TEST_NAME=
	echo * Please enter a test name, or hit ENTER to run all tests:
	set /P TEST_NAME=* e.g. APP.TEST_CLASS.TEST_METHOD:
	set APPLICATION_DB=test_mentor5_test
	echo Using %APPLICATION_DB% as test database...
	"%POSTGRES_BIN%\dropdb.exe" -U postgres %APPLICATION_DB%
	"%POSTGRES_BIN%\createdb.exe" -U postgres %APPLICATION_DB%
	cd %APPLICATION_SRC%
	echo Tests commencing...
	python manage.py test %TEST_NAME%
	echo Cleaning up test database %APPLICATION_DB%...
	"%POSTGRES_BIN%\dropdb.exe" -U postgres %APPLICATION_DB%
	echo Done!
	GOTO DO_MORE

:DO_MORE
	set ITEM=
	REM SET /P ITEM=* Perform other operations? (y/n):
	REM IF %ITEM% == y GOTO DO_MENU
	REM IF %ITEM% == Y GOTO DO_MENU
	REM IF %ITEM% == yes GOTO DO_MENU
	REM IF %ITEM% == Yes GOTO DO_MENU
	REM IF %ITEM% == YES GOTO DO_MENU
	REM GOTO END
	echo *
	GOTO DO_MENU

:FINISH_UP
	cd %WORKSPACE%\..\bin
	echo *
	pause
	GOTO END

:QUIT
	echo *
	echo * No actions were performed.
	echo *
	GOTO END

:END
	echo * Finished.