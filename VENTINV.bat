@echo off
if "%~1"=="hidden" goto :run

set VBS=%temp%\oculto_%random%.vbs
echo Set objShell = CreateObject("WScript.Shell") > "%VBS%"
echo objShell.Run "cmd /c """"%~f0"""" hidden", 0, False >> "%VBS%"
wscript "%VBS%"
del "%VBS%"
exit

:run
cd /d "C:\Users\TV\Documents\VENTINV"
call "C:\Users\TV\Documents\VENTINV\venv\Scripts\activate.bat"
start "" http://127.0.0.1:8000/
python manage.py runserver