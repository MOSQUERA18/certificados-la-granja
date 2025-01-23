from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, WebDriverException
import time
import traceback
import pandas as pd
from dotenv import load_dotenv
import os
from leerEXCEL import leer_excel
from generarResultados import generar_resultados

# Cargar las variables de entorno
load_dotenv()

def automatizar_navegacion(datos):
    driver = None
    resultados = []

    try:
        # Obtener ruta del chromedriver y URL desde .env
        ruta_chromedriver = os.getenv("CHROMEDRIVER_PATH")
        url = os.getenv("CERTIFICADO_URL")

        if not ruta_chromedriver or not url:
            raise ValueError("Faltan variables de entorno en el archivo .env")

        service = Service(ruta_chromedriver)
        driver = webdriver.Chrome(service=service)
        driver.get(url)

        fila_actual = 0

        while fila_actual < len(datos):
            try:
                driver.get(url)

                row = datos.iloc[fila_actual]
                print(f"Procesando fila {fila_actual + 1}...")

                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[text()='Expedición Certificado']"))
                ).click()

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_TextBox1"))
                ).send_keys(str(row["NUMERO DE DOCUMENTO"]))

                Select(WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList1"))
                )).select_by_visible_text(str(row["DIA"]).zfill(2))

                mes_normalizado = str(row["MES"]).capitalize()
                Select(WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList2"))
                )).select_by_visible_text(mes_normalizado)

                Select(WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList3"))
                )).select_by_visible_text(str(row["AÑO"]))

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_TextBox2"))
                ).send_keys("LANAP")

                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_Button1"))
                ).click()

                try:
                    mensaje_error = WebDriverWait(driver, 5).until(
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
                        continue

                except TimeoutException:
                    pass

                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_Button1"))
                ).click()

                print(f"Certificado generado correctamente para la fila {fila_actual + 1}.")
                resultados.append({
                    "STATUS": "EXITO",
                    "OBSERVACIONES": "Certificado generado correctamente"
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

if __name__ == "__main__":
    archivo_usuario = input("Ingrese el nombre del archivo Excel con los datos: ")
    datos = leer_excel(archivo_usuario)
    if datos is not None:
        automatizar_navegacion(datos)
