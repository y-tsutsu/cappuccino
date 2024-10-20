@echo off

set WORK=%~dp0
cd /d %WORK%

python -m nuitka --standalone --onefile --windows-console-mode=disable ^
--windows-icon-from-ico=cappuccino.ico --enable-plugin=pyside6 --include-qt-plugins=qml ^
--include-data-dir=qml=qml --include-data-files=cappuccino.ico=cappuccino.ico cappuccino.py
