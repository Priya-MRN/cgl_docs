@echo off
REM ===================================================================
REM  Daily Current Affairs Digest - launcher
REM  Mines headlines, buckets them (Sports/Days/Summits/Agreements/
REM  Awards), renders a dated PDF, and auto commits+pushes to git.
REM  Called by Task Scheduler.
REM ===================================================================
cd /d "%~dp0"
"C:\Users\PRIYA\AppData\Local\Python\pythoncore-3.14-64\python.exe" "%~dp0daily_ca_digest.py" %*
exit /b %ERRORLEVEL%
