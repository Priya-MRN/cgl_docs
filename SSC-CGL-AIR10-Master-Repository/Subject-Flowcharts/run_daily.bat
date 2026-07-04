@echo off
REM ===================================================================
REM  Subject-Flowchart daily updater - launcher
REM  Stamps today's date + rotating focus into the 5 study pages,
REM  and mines today's Current-Affairs headlines into the CA page.
REM  Called by Windows Task Scheduler (or run by hand).
REM
REM    run_daily.bat            full run (stamp + rotate + mine news)
REM    run_daily.bat --no-news  offline (just stamp date + rotate focus)
REM ===================================================================
cd /d "%~dp0"
"C:\Users\PRIYA\AppData\Local\Python\pythoncore-3.14-64\python.exe" "%~dp0subject_daily.py" %*
exit /b %ERRORLEVEL%
