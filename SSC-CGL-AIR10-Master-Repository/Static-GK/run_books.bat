@echo off
REM ===================================================================
REM  Daily Book-Releases updater - launcher
REM  Mines GKToday for book headlines, refreshes Books-and-Authors.html.
REM  Called by Windows Task Scheduler.
REM ===================================================================
cd /d "%~dp0"
"C:\Users\PRIYA\AppData\Local\Python\pythoncore-3.14-64\python.exe" "%~dp0books_daily.py" %*
exit /b %ERRORLEVEL%
