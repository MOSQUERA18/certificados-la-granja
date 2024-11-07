const express = require('express');
const multer = require('multer');
const xlsx = require('xlsx');
const puppeteer = require('puppeteer');
const tesseract = require('tesseract.js');  // OCR para detectar el CAPTCHA
const fs = require('fs');
const path = require('path');
const cors = require('cors');

// Inicializar Express
const app = express();
const upload = multer({ dest: 'uploads/' });
app.use(cors());

// Crear la carpeta 'certificados' si no existe
const certificadosDir = path.join(__dirname, 'certificados');
if (!fs.existsSync(certificadosDir)) {
  console.log(`Creando directorio: ${certificadosDir}`);
  fs.mkdirSync(certificadosDir);
}

// Ruta para subir y procesar el archivo de Excel
app.post('/upload', upload.single('file'), async (req, res) => {
  try {
    const filePath = req.file.path;

    // Leer el archivo Excel
    const workbook = xlsx.readFile(filePath);
    const sheet_name_list = workbook.SheetNames;
    const sheet = xlsx.utils.sheet_to_json(workbook.Sheets[sheet_name_list[0]]);

    // Iterar sobre cada fila del Excel
    for (let row of sheet) {
      const { cedula, fechaExpedicionDia, fechaExpedicionMes, fechaExpedicionAno, tipoDocumento } = row;

      if (tipoDocumento === 'Cedula') {
        console.log("entrando al modo de generar cedulas");
        await generarCertificadoCedula(cedula, { dia: fechaExpedicionDia, mes: fechaExpedicionMes, ano: fechaExpedicionAno });
      } else if (tipoDocumento === 'Tarjeta de Identidad') {
        await generarCertificadoTarjeta(cedula, { dia: fechaExpedicionDia, mes: fechaExpedicionMes, ano: fechaExpedicionAno });
      }
    }

    res.send('Certificados generados exitosamente');
  } catch (error) {
    console.error('Error al procesar el archivo:', error);
    res.status(500).send('Error al procesar el archivo');
  }
});

async function generarCertificadoCedula(cedula, fechaExpedicion) {
  try {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    await page.goto('https://certvigenciacedula.registraduria.gov.co/Datos.aspx');

    // Llenar los campos del formulario
    await page.type('#ContentPlaceHolder1_TextBox1', cedula);
    await page.select('#ContentPlaceHolder1_DropDownList1', fechaExpedicion.dia);
    await page.select('#ContentPlaceHolder1_DropDownList2', fechaExpedicion.mes);
    await page.select('#ContentPlaceHolder1_DropDownList3', fechaExpedicion.ano);

    // Esperar que el CAPTCHA esté presente
    await page.waitForSelector('#datos_contentplaceholder1_captcha1_CaptchaImage');
    const captchaElement = await page.$('#datos_contentplaceholder1_captcha1_CaptchaImage');
    const captchaPath = path.join(certificadosDir, 'captcha.png');
    await captchaElement.screenshot({ path: captchaPath });

    // Usar Tesseract para leer el CAPTCHA
    const result = await tesseract.recognize(captchaPath, 'eng');
    const captchaText = result.data && result.data.text ? result.data.text.trim() : null; // Manejo seguro de la respuesta

    if (!captchaText) {
      throw new Error('No se pudo detectar texto en el CAPTCHA');
    }

    console.log(`CAPTCHA detectado: ${captchaText}`);

    // Llenar el campo del CAPTCHA con el texto detectado
    await page.type('#ContentPlaceHolder1_TextBox2', captchaText);

    // Continuar con el flujo
    await page.click('#ContentPlaceHolder1_Button1');

    // Esperar el enlace de descarga
    await page.waitForSelector('a[download]');
    
    // Obtener el enlace del PDF
    const downloadLink = await page.$eval('a[download]', a => a.href);
    console.log(`Enlace del PDF: ${downloadLink}`);

    // Descargar el PDF usando Axios
    const response = await axios({
      url: downloadLink,
      method: 'GET',
      responseType: 'stream',
    });
    const pdfPath = path.join(certificadosDir, `${cedula}.pdf`);
    response.data.pipe(fs.createWriteStream(pdfPath));

    console.log(`Certificado guardado en ${pdfPath}`);

    await browser.close();
    console.log(`Certificado para cédula ${cedula} guardado en ${pdfPath}`);
  } catch (error) {
    console.error(`Error al generar certificado para la cédula ${cedula}:`, error.message);
  }
}

// Función para generar certificados de Tarjeta de Identidad en PDF
async function generarCertificadoTarjeta(cedula, fechaExpedicion) {
  try {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    // Ir a la página y completar los formularios
    await page.goto('https://consultasrc.registraduria.gov.co:28080/ProyectoSCCRC/');
    await page.type('#cedula', cedula);
    await page.select('#dia', fechaExpedicion.dia);
    await page.select('#mes', fechaExpedicion.mes);
    await page.select('#ano', fechaExpedicion.ano);

    // Capturar la imagen del CAPTCHA
    const captchaElement = await page.$('#captchaImage');
    const captchaPath = path.join(certificadosDir, 'captcha.png');
    await captchaElement.screenshot({ path: captchaPath });

    // Usar Tesseract para leer el CAPTCHA
    const { data: { text } } = await tesseract.recognize(captchaPath, 'eng');
    const captchaCode = text.trim();

    console.log(`CAPTCHA detectado: ${captchaCode}`);

    // Introducir el código CAPTCHA en el formulario
    await page.type('#codigo', captchaCode);

    // Continuar con el flujo
    await page.click('#continuar');
    await page.waitForSelector('a[download]');

    // Guardar el PDF con el nombre del número de cédula
    const pdfPath = path.join(certificadosDir, `${cedula}.pdf`);
    console.log(`Generando PDF en: ${pdfPath}`);
    await page.pdf({ path: pdfPath, format: 'A4' });

    await browser.close();
    console.log(`Certificado para tarjeta de identidad ${cedula} guardado en ${pdfPath}`);
  } catch (error) {
    console.error(`Error al generar certificado para la tarjeta de identidad ${cedula}:`, error);
  }
}

// Iniciar el servidor
app.listen(3000, () => {
  console.log('Servidor corriendo en http://localhost:3000');
});
