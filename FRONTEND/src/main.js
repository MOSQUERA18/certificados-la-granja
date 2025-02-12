import { app, BrowserWindow } from 'electron';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const _dirname = path.dirname(__filename);

// Cargar las variables de entorno
dotenv.config();

let mainWindow;
console.log(_dirname)
app.whenReady().then(() => {
    mainWindow = new BrowserWindow({
        width: 600,
        height: 550,
        webPreferences: {
            nodeIntegration: true
        },
        icon: path.join(_dirname, '../public/Logo.ico') 
    });



    mainWindow.setMenuBarVisibility(false);


    // Usar la URL desde el .env
    const frontendURL = process.env.FRONTEND_URL
    mainWindow.loadURL(frontendURL);
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
