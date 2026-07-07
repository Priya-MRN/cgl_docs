@echo off
REM ===================================================================
REM  Daily GK Current-Affairs Digest (gknow.in) - launcher
REM  Scrapes 8 gknow.in category feeds (headlines + descriptions),
REM  merges the curated notes, renders one combined PDF, and auto
REM  commits+pushes to git. Called by Task Scheduler.
REM ===================================================================
cd /d "%~dp0"
"C:\Users\PRIYA\AppData\Local\Python\pythoncore-3.14-64\python.exe" "%~dp0daily_gk_digest.py" %*
exit /b %ERRORLEVEL%
