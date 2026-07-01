@echo off
REM ===================================================================
REM  Daily One-Word Substitution - launcher
REM  Runs the OWS builder. Called by Windows Task Scheduler.
REM ===================================================================
cd /d "%~dp0"
"C:\Users\PRIYA\AppData\Local\Python\pythoncore-3.14-64\python.exe" "%~dp0ows_daily.py" %*
exit /b %ERRORLEVEL%
