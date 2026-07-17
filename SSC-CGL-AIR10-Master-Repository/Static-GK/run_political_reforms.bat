@echo off
REM ===================================================================
REM  Political Reforms & Reformers - daily launcher
REM  Renders the curated CM/minister/reformer capsule + mines fresh
REM  in-scope GKToday political headlines, builds one dated PDF, and
REM  auto commits+pushes to git.
REM  Called by Task Scheduler.
REM ===================================================================
cd /d "%~dp0"
"C:\Users\PRIYA\AppData\Local\Python\pythoncore-3.14-64\python.exe" "%~dp0daily_political_reforms.py" %*
exit /b %ERRORLEVEL%
