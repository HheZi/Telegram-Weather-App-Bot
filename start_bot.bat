@echo off
REM 
call venv\Scripts\activate

REM
python ./src/bot.py

REM 
call venv\Scripts\deactivate
pause

