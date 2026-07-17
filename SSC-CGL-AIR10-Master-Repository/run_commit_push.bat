@echo off
REM ===================================================================
REM  Daily end-of-day git sweep - launcher
REM  Runs AFTER all other daily tasks: stages every change, commits with
REM  a dated message, and pushes to origin/main (unattended).
REM  Called by Task Scheduler.
REM ===================================================================
cd /d "%~dp0"
"C:\Users\PRIYA\AppData\Local\Python\pythoncore-3.14-64\python.exe" "%~dp0daily_commit_push.py" %*
exit /b %ERRORLEVEL%
