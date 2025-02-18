import { app, BrowserWindow, ipcMain } from 'electron';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import path from 'path';
import os from 'os';0

const __filename = fileURLToPath(import.meta.url);
const _dirname = path.dirname(__filename);

// Cargar las variables de entorno
//dotenv.config();

let mainWindow;

app.whenReady().then(() => {
    mainWindow = new BrowserWindow({
        width: 600,
        height: 550,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true // Asegúrate de que esto esté configurado correctamente según tus necesidades de seguridad
        },
        icon: path.join(_dirname, '../public/Logo.ico') 
    });

    //mainWindow.setMenuBarVisibility(false);

    const indexPath = path.join(_dirname, '../index.html');
    console.log("indexPath: " + indexPath)
    mainWindow.loadURL("http://localhost:5173/");
    
    // Manejar la descarga de archivos
    mainWindow.webContents.session.on('will-download', (event, item, webContents) => {
        const downloadsPath = path.join(os.homedir(), 'Downloads'); // Ruta de la carpeta de Descargas
        const filePath = path.join(downloadsPath, item.getFilename()); // Ruta completa del archivo

        // Establecer la ruta de destino
        item.setSavePath(filePath);

        // Opcional: Puedes mostrar el progreso de la descarga
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
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});