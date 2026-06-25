@echo off
REM ===================================================================
REM  Daily Editorial Vocabulary - launcher
REM  Runs the Python generator. Called by Windows Task Scheduler.
REM ===================================================================
cd /d "%~dp0"
"C:\Users\PRIYA\AppData\Local\Python\pythoncore-3.14-64\python.exe" "%~dp0daily_vocab.py" %*
exit /b %ERRORLEVEL%
