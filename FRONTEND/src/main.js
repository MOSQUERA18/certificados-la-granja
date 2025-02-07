import { app, BrowserWindow } from 'electron';
import dotenv from 'dotenv';

// Cargar las variables de entorno
dotenv.config();

let mainWindow;

app.whenReady().then(() => {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    });

    // Usar la URL desde el .env
    const frontendURL = process.env.FRONTEND_URL
    mainWindow.loadURL(frontendURL);
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
