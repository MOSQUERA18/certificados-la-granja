@echo off
cd /d "%~dp0"
echo Iniciando la aplicación...

:: Iniciar backend y frontend en una nueva ventana
start cmd /k "npm run dev"

:: Esperar unos segundos para que el servidor inicie
timeout /t 5 /nobreak >nul

:: Abrir el navegador con el frontend
start "" "http://localhost:5173"

:: Cerrar este script sin cerrar la consola
exit