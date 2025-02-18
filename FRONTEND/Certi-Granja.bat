@echo off
cd /d "%~dp0"
echo Iniciando la aplicación...

:: 1️⃣ Iniciar backend y frontend con npm run dev (que ya los ejecuta ambos)
start /b cmd /c "npm run dev"

:: Esperar unos segundos para que todo se inicie
timeout /t 5 /nobreak >nul

:: 2️⃣ Abrir el navegador con el frontend usando Certi-Granja.local
start "" "http://localhost:5173"

:: Cerrar el script para que no quede CMD abierto
exit
