import { app, BrowserWindow } from 'electron';

let mainWindow;

app.whenReady().then(() => {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    });

    mainWindow.loadURL('http://localhost:5173'); // Asegúrate de que este puerto es correcto
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
