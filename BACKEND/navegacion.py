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
from unir_certificados import unir_pdfs

# Cargar las variables de entorno
load_dotenv()

def obtener_enlace_tipo_documento(tipo_documento):
    """
    Retorna el enlace correspondiente según el tipo de documento
    """
    enlaces = {
        "TI": "https://consultasrc.registraduria.gov.co/ProyectoSCCRC/faces/index.xhtml",
        "CE": "https://apps.migracioncolombia.gov.co/consultaCedulas/pages/home.jsf - victor.echeverry@cancilleria.gov.co",
        "PPT": "https://apps.migracioncolombia.gov.co:8443/consultappt/"
    }
    return enlaces.get(tipo_documento, "")

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
                row = datos.iloc[fila_actual]
                tipo_documento = str(row["TIPO DE DOCUMENTO"]).strip().upper()
                
                # Verificar si es un tipo de documento especial (CE, PPT, TI)
                if tipo_documento in ["CE", "PPT", "TI"]:
                    enlace = obtener_enlace_tipo_documento(tipo_documento)
                    print(f"Fila {fila_actual + 1}: Tipo de documento {tipo_documento} - Agregando enlace especial")
                    resultados.append({
                        "STATUS": "ENLACE_ESPECIAL",
                        "OBSERVACIONES": f"Este tipo de certificado ({tipo_documento}) se genera en: {enlace}"
                    })
                    fila_actual += 1
                    continue
                
                driver.get(url)
                
                # Verificar si el mensaje de error está presente
                try:
                    WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, "//h3[text()='Al parecer se presentó algun problema!']"))
                    )
                    print(f"Se presentó un problema en la fila {fila_actual + 1}. Continuando con la siguiente fila...")
                    # AGREGAR RESULTADO ANTES DE INCREMENTAR - ESTA ES LA CORRECCIÓN
                    resultados.append({
                        "STATUS": "ERROR DE PAGINA",
                        "OBSERVACIONES": "Se presentó un problema en la página"
                    })
                    fila_actual += 1
                    continue  # Saltar a la siguiente fila
                except TimeoutException:
                    pass  # No se encontró el mensaje, continuar con el proceso normal

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
                        continue  # MANTENER TU LÓGICA ORIGINAL DE REINTENTO
                        
                except TimeoutException:
                    pass
                                
                WebDriverWait(driver, 1).until(  # Reducido a 5 segundos
                    EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_Button1"))
                ).click()
                
                # Verificar si hay una novedad
                try:
                    novedad_element = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_Label11"))
                    )
                    if novedad_element.is_displayed():
                        texto_novedad = novedad_element.text.strip()
                        print(f"Novedad detectada en la fila {fila_actual + 1}: {texto_novedad}")
                        resultados.append({
                            "STATUS": "NOVEDAD",
                            "OBSERVACIONES": f"NOVEDAD: {texto_novedad}"
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
                    # CORREGIR: Modificar el último resultado si ya existe, no agregar uno nuevo
                    if resultados and len(resultados) > 0:
                        resultados[-1] = {
                            "STATUS": "ERROR DE PAGINA",
                            "OBSERVACIONES": "Certificado no se generó por Error de la pagina"
                        }
                    else:
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
        
        # Unir los PDFs en la carpeta de destino (usando la función importada)
        if carpeta_destino:
            unir_pdfs(carpeta_destino)
    
    return resultados

if __name__ == "__main__":
    archivo_usuario = input("Ingrese el nombre del archivo Excel con los datos: ")
    datos = leer_excel(archivo_usuario)
    if datos is not None:
        automatizar_navegacion(datos)