@echo off
title VENTINV - Servidor de Desarrollo
cd /d "c:\Users\TV\Documents\VENTINV"
echo Iniciando servidor de VENTINV...
echo Abriendo navegador en http://127.0.0.1:8000/
timeout /t 3 >nul
start "" "http://127.0.0.1:8000/"
venv\Scripts\python.exe manage.py runserver
pause
