@echo off
REM ===================================================================
REM  Summits / Events / Sports / IR / Inventions - daily launcher
REM  Renders the frozen 2-year capsule + mines fresh in-scope GKToday
REM  headlines, builds one dated PDF, and auto commits+pushes to git.
REM  Called by Task Scheduler.
REM ===================================================================
cd /d "%~dp0"
"C:\Users\PRIYA\AppData\Local\Python\pythoncore-3.14-64\python.exe" "%~dp0daily_summits_events.py" %*
exit /b %ERRORLEVEL%
