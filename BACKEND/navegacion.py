from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import time
import traceback
import pandas as pd
from dotenv import load_dotenv
import os
import glob
from leerEXCEL import leer_excel
from generarResultados import generar_resultados
import shutil
import PyPDF2  # Asegúrate de importar PyPDF2 al inicio del archivo

# Cargar las variables de entorno
load_dotenv()

def unir_pdfs(carpeta_destino):
    import re

    pdf_files = glob.glob(os.path.join(carpeta_destino, "*.pdf"))
    pdf_writer = PyPDF2.PdfWriter()
    cedulas_agregadas = set()

    for pdf_file in pdf_files:
        with open(pdf_file, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                texto = page.extract_text()

                # Buscar la cédula en el texto usando regex
                match = re.search(r"Cédula de Ciudadanía:\s+([\d\.]+)", texto)
                if match:
                    cedula = match.group(1).replace('.', '')

                    # Solo añadir si no está repetida
                    if cedula not in cedulas_agregadas:
                        pdf_writer.add_page(page)
                        cedulas_agregadas.add(cedula)
                    else:
                        print(f"Certificado duplicado omitido: {cedula}")
                else:
                    print("No se encontró la cédula en una página. Página agregada por precaución.")
                    pdf_writer.add_page(page)

    output_pdf_path = os.path.join(carpeta_destino, "CERTIFICADOS_UNIDOS.pdf")
    with open(output_pdf_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"PDF generado sin duplicados: {output_pdf_path}")

def automatizar_navegacion(datos, carpeta_destino=None):
    driver = None
    resultados = []

    try:
        # Obtener URL desde .env
        url = os.getenv("CERTIFICADO_URL")

        if not url:
            raise ValueError("Faltan variables de entorno en el archivo .env")

        # Configurar el driver usando webdriver-manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)          
        driver.get(url)

        fila_actual = 0

        while fila_actual < len(datos):
            try:
                driver.get(url)

                # Verificar si el mensaje de error está presente
                try:
                    WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, "//h3[text()='Al parecer se presentó algun problema!']"))
                    )
                    print(f"Se presentó un problema en la fila {fila_actual + 1}. Continuando con la siguiente fila...")
                    fila_actual += 1
                    continue  # Saltar a la siguiente fila
                except TimeoutException:
                    pass  # No se encontró el mensaje, continuar con el proceso normal

                row = datos.iloc[fila_actual]
                print(f"Procesando fila {fila_actual + 1}...")

                WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[text()='Expedición Certificado']"))
                ).click()

                WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_TextBox1"))
                ).send_keys(str(row["NUMERO DE DOCUMENTO"]))
                                                                                                                                                                                                                                                                                                                                      
                Select(WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList1"))
                )).select_by_visible_text(str(row["DIA"]).zfill(2))

                mes_normalizado = str(row["MES"]).capitalize()
                Select(WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList2"))
                )).select_by_visible_text(mes_normalizado)

                Select(WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList3"))
                )).select_by_visible_text(str(row["AÑO"]))

                WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_TextBox2"))
                ).send_keys("LANAP")

                WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_Button1"))
                ).click()

                # Esperar un momento para que el PDF se genere
                time.sleep(1)  # Ajusta el tiempo según sea necesario
                try:
                    mensaje_error = WebDriverWait(driver, 1).until(  # Reducido a 3 segundos
                        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_Label11"))
                    ).text

                    if "El número de documento no se encuentra en la base de datos" in mensaje_error:
                        print(f"Error en la fila {fila_actual + 1}: {mensaje_error}")
                        resultados.append({
                            "STATUS": "FALLIDO",
                            "OBSERVACIONES": "Número de documento o fecha de expedición erróneas"
                        })
                        fila_actual += 1
                        continue

                    if "CAPTCHA" in mensaje_error:
                        print(f"Error de CAPTCHA en la fila {fila_actual + 1}. Reintentando...")
                        # Aquí puedes implementar un contador de reintentos si lo deseas
                        continue

                except TimeoutException:
                    pass
                
                WebDriverWait(driver, 1).until(  # Reducido a 5 segundos
                    EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_Button1"))
                ).click()

                # Verificar si hay una novedad
                try:
                    novedad_element = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_Label12"))
                    )
                    if novedad_element.is_displayed():
                        print(f"Novedad detectada en la fila {fila_actual + 1}.")
                        resultados.append({
                            "STATUS": "NOVEDAD",
                            "OBSERVACIONES": "Esta persona tiene una novedad en su certificado"
                        })
                    else:
                        resultados.append({
                            "STATUS": "EXITO",
                            "OBSERVACIONES": "Certificado generado correctamente"
                        })
                except TimeoutException:
                    resultados.append({
                        "STATUS": "EXITO",
                        "OBSERVACIONES": "Certificado generado correctamente"
                    })

                # Verificar si el archivo PDF se ha descargado
                downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
                pdf_filename_pattern = f"Certificado estado cedula {str(row['NUMERO DE DOCUMENTO'])}*.pdf"

                # Esperar hasta que el archivo PDF se descargue
                pdf_path = None
                for _ in range(10):  # Intentar hasta 10 veces
                    pdf_path = glob.glob(os.path.join(downloads_folder, pdf_filename_pattern))
                    if pdf_path:
                        break
                    time.sleep(1)  # Esperar 1 segundo entre intentos

                if pdf_path:
                    print(f"Certificado generado correctamente para la fila {fila_actual + 1}.")
                    # Mover el archivo PDF a la carpeta de destino
                    if carpeta_destino:
                        for file in pdf_path:
                            shutil.move(file, carpeta_destino)
                            print(f"Archivo PDF movido a: {carpeta_destino}")
                else:
                    print(f"Certificado no encontrado para la fila {fila_actual + 1}.")
                    resultados.append({
                        "STATUS": "ERROR DE PAGINA",
                        "OBSERVACIONES": "Certificado no se generó por Error de la pagina"
                    })

                fila_actual += 1

            except WebDriverException as e:
                print("Automatización completada con éxito.")
            continue

    except Exception as main_exception:
        print(f"Error general durante la ejecución: {main_exception}")
        traceback.print_exc()
    finally:
        if driver:
            print("Esperando unos segundos para asegurar descargas completas...")
            time.sleep(1)
            driver.quit()

        # Obtener nombre del archivo desde .env
        nombre_archivo = os.getenv("OUTPUT_FILE", "resultados_certificados.xlsx")
        resultados_df = pd.DataFrame(resultados)
        generar_resultados(datos, resultados_df, nombre_archivo)

        # Unir los PDFs en la carpeta de destino
        if carpeta_destino:
            unir_pdfs(carpeta_destino)

    return resultados  

if __name__ == "__main__":
    archivo_usuario = input("Ingrese el nombre del archivo Excel con los datos: ")
    datos = leer_excel(archivo_usuario)
    if datos is not None:
        automatizar_navegacion(datos)
