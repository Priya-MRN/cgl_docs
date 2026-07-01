@echo off
REM ===================================================================
REM  Daily GK / Current Affairs - launcher
REM  Scrapes GKToday and rebuilds the HTML. Called by Task Scheduler.
REM ===================================================================
cd /d "%~dp0"
"C:\Users\PRIYA\AppData\Local\Python\pythoncore-3.14-64\python.exe" "%~dp0gk_daily.py" %*
exit /b %ERRORLEVEL%
