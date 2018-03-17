@echo off

set BKPATH=%CD%
set WORK=%~dp0
cd /d %WORK%

REM pyinstaller.exe cappuccino.py --onefile --noconsole --clean --icon=cappuccino.ico
pyinstaller.exe cappuccino.spec

cd %BKPATH%
