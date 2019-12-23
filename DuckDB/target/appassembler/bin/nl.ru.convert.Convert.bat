@REM ----------------------------------------------------------------------------
@REM  Copyright 2001-2006 The Apache Software Foundation.
@REM
@REM  Licensed under the Apache License, Version 2.0 (the "License");
@REM  you may not use this file except in compliance with the License.
@REM  You may obtain a copy of the License at
@REM
@REM       http://www.apache.org/licenses/LICENSE-2.0
@REM
@REM  Unless required by applicable law or agreed to in writing, software
@REM  distributed under the License is distributed on an "AS IS" BASIS,
@REM  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@REM  See the License for the specific language governing permissions and
@REM  limitations under the License.
@REM ----------------------------------------------------------------------------
@REM
@REM   Copyright (c) 2001-2006 The Apache Software Foundation.  All rights
@REM   reserved.

@echo off

set ERROR_CODE=0

:init
@REM Decide how to startup depending on the version of windows

@REM -- Win98ME
if NOT "%OS%"=="Windows_NT" goto Win9xArg

@REM set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" @setlocal

@REM -- 4NT shell
if "%eval[2+2]" == "4" goto 4NTArgs

@REM -- Regular WinNT shell
set CMD_LINE_ARGS=%*
goto WinNTGetScriptDir

@REM The 4NT Shell from jp software
:4NTArgs
set CMD_LINE_ARGS=%$
goto WinNTGetScriptDir

:Win9xArg
@REM Slurp the command line arguments.  This loop allows for an unlimited number
@REM of arguments (up to the command line limit, anyway).
set CMD_LINE_ARGS=
:Win9xApp
if %1a==a goto Win9xGetScriptDir
set CMD_LINE_ARGS=%CMD_LINE_ARGS% %1
shift
goto Win9xApp

:Win9xGetScriptDir
set SAVEDIR=%CD%
%0\
cd %0\..\.. 
set BASEDIR=%CD%
cd %SAVEDIR%
set SAVE_DIR=
goto repoSetup

:WinNTGetScriptDir
set BASEDIR=%~dp0\..

:repoSetup
set REPO=


if "%JAVACMD%"=="" set JAVACMD=java

if "%REPO%"=="" set REPO=%BASEDIR%\repo

set CLASSPATH="%BASEDIR%"\etc;"%REPO%"\org\apache\lucene\lucene-core\8.3.0\lucene-core-8.3.0.jar;"%REPO%"\org\apache\lucene\lucene-benchmark\8.3.0\lucene-benchmark-8.3.0.jar;"%REPO%"\org\apache\lucene\lucene-analyzers-common\8.3.0\lucene-analyzers-common-8.3.0.jar;"%REPO%"\org\apache\lucene\lucene-codecs\8.3.0\lucene-codecs-8.3.0.jar;"%REPO%"\org\apache\lucene\lucene-facet\8.3.0\lucene-facet-8.3.0.jar;"%REPO%"\org\apache\lucene\lucene-highlighter\8.3.0\lucene-highlighter-8.3.0.jar;"%REPO%"\org\apache\lucene\lucene-join\8.3.0\lucene-join-8.3.0.jar;"%REPO%"\org\apache\lucene\lucene-memory\8.3.0\lucene-memory-8.3.0.jar;"%REPO%"\org\apache\lucene\lucene-queries\8.3.0\lucene-queries-8.3.0.jar;"%REPO%"\org\apache\lucene\lucene-queryparser\8.3.0\lucene-queryparser-8.3.0.jar;"%REPO%"\org\apache\lucene\lucene-spatial-extras\8.3.0\lucene-spatial-extras-8.3.0.jar;"%REPO%"\com\ibm\icu\icu4j\62.1\icu4j-62.1.jar;"%REPO%"\net\sourceforge\nekohtml\nekohtml\1.9.17\nekohtml-1.9.17.jar;"%REPO%"\org\apache\commons\commons-compress\1.18\commons-compress-1.18.jar;"%REPO%"\org\locationtech\spatial4j\spatial4j\0.7\spatial4j-0.7.jar;"%REPO%"\xerces\xercesImpl\2.9.1\xercesImpl-2.9.1.jar;"%REPO%"\org\apache\lucene\lucene-test-framework\8.3.0\lucene-test-framework-8.3.0.jar;"%REPO%"\com\carrotsearch\randomizedtesting\randomizedtesting-runner\2.7.2\randomizedtesting-runner-2.7.2.jar;"%REPO%"\junit\junit\4.12\junit-4.12.jar;"%REPO%"\org\hamcrest\hamcrest-core\1.3\hamcrest-core-1.3.jar;"%REPO%"\args4j\args4j\2.32\args4j-2.32.jar;"%REPO%"\org\apache\logging\log4j\log4j-api\2.4\log4j-api-2.4.jar;"%REPO%"\org\apache\logging\log4j\log4j-core\2.4\log4j-core-2.4.jar;"%REPO%"\org\jetbrains\annotations\18.0.0\annotations-18.0.0.jar;"%REPO%"\squirrel\olddog\1.0-SNAPSHOT\olddog-1.0-SNAPSHOT.jar

set ENDORSED_DIR=
if NOT "%ENDORSED_DIR%" == "" set CLASSPATH="%BASEDIR%"\%ENDORSED_DIR%\*;%CLASSPATH%

if NOT "%CLASSPATH_PREFIX%" == "" set CLASSPATH=%CLASSPATH_PREFIX%;%CLASSPATH%

@REM Reaching here means variables are defined and arguments have been captured
:endInit

%JAVACMD% %JAVA_OPTS%  -classpath %CLASSPATH% -Dapp.name="nl.ru.convert.Convert" -Dapp.repo="%REPO%" -Dapp.home="%BASEDIR%" -Dbasedir="%BASEDIR%" nl.ru.convert.Convert %CMD_LINE_ARGS%
if %ERRORLEVEL% NEQ 0 goto error
goto end

:error
if "%OS%"=="Windows_NT" @endlocal
set ERROR_CODE=%ERRORLEVEL%

:end
@REM set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" goto endNT

@REM For old DOS remove the set variables from ENV - we assume they were not set
@REM before we started - at least we don't leave any baggage around
set CMD_LINE_ARGS=
goto postExec

:endNT
@REM If error code is set to 1 then the endlocal was done already in :error.
if %ERROR_CODE% EQU 0 @endlocal


:postExec

if "%FORCE_EXIT_ON_ERROR%" == "on" (
  if %ERROR_CODE% NEQ 0 exit %ERROR_CODE%
)

exit /B %ERROR_CODE%
