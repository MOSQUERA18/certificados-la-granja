import { app, BrowserWindow } from 'electron';
import path from 'path';
import { exec } from 'child_process';
import os from 'os';
import { fileURLToPath } from 'url';

let mainWindow;
let backendProcess;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Función para iniciar el backend en Flask
function startPythonBackend() {
    return new Promise((resolve, reject) => {
        const backendPath = path.join(__dirname, '..', '..', 'backend', 'app.py');  // Ruta correcta a tu app.py

        console.log(`Iniciando backend con el archivo: ${backendPath}`);

        backendProcess = exec(`python "${backendPath}"`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error ejecutando el backend: ${error.message}`);
                reject(error);
                return;
            }
            if (stderr) {
                console.error(`Error en backend: ${stderr}`);
                reject(stderr);
                return;
            }
            console.log(`Backend iniciado: ${stdout}`);
        });

        backendProcess.stdout.on('data', (data) => {
            console.log(`Backend stdout: ${data}`);
            if (data.includes('Running on')) {  // Verifica que el backend esté corriendo
                console.log("Backend ha arrancado correctamente.");
                resolve();
            }
        });

        backendProcess.stderr.on('data', (data) => {
            console.error(`Backend stderr: ${data}`);
        });
    });
}

// Función para crear la ventana principal de la aplicación
async function createWindow() {
    try {
        // await startPythonBackend();  // Espera que el backend se inicie correctamente
        console.log("✅ Backend iniciado correctamente");

        mainWindow = new BrowserWindow({
            width: 800,
            height: 600,
            webPreferences: {
                nodeIntegration: true,
                contextIsolation: false
            },
            icon: path.join(app.getAppPath(), 'public', 'Logo.ico')
        });

        mainWindow.setMenuBarVisibility(false);

        const startURL = process.env.NODE_ENV === 'development'
            ? 'http://localhost:5173/'  // Carga el frontend en desarrollo
            : `http://localhost:5173/`;  // Carga el frontend en producción

        console.log(`Cargando frontend desde: ${startURL}`);
        mainWindow.loadURL(startURL);  // Carga el frontend en la ventana de Electron

        mainWindow.webContents.openDevTools();  // Abre las herramientas de desarrollo
    } catch (error) {
        console.error("🚨 Error al iniciar la aplicación:", error);
    }

    // Manejar la descarga de archivos
    mainWindow.webContents.session.on('will-download', (event, item, webContents) => {
        const downloadsPath = path.join(os.homedir(), 'Downloads');
        const filePath = path.join(downloadsPath, item.getFilename());

        item.setSavePath(filePath);

        item.on('updated', (event, state) => {
            if (state === 'interrupted') {
                console.log('Descarga interrumpida');
            } else if (state === 'progressing') {
                if (item.isPaused()) {
                    console.log('Descarga en pausa');
                } else {
                    console.log(`Descargando... ${item.getReceivedBytes()} bytes recibidos`);
                }
            }
        });

        item.once('done', (event, state) => {
            if (state === 'completed') {
                console.log('Descarga completada');
            } else {
                console.log(`Descarga fallida: ${state}`);
            }
        });
    });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (backendProcess) {
        backendProcess.kill();  // Matar el proceso del backend al cerrar la aplicación
    }

    // Cerrar el frontend (Vite)
    exec('taskkill /F /IM node.exe /T', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error al cerrar procesos: ${error.message}`);
        }
    });

    app.quit();
});
