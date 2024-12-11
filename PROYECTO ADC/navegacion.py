from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import traceback
from leerEXCEL import leer_excel

def automatizar_navegacion(datos):
    driver = None
    try:
        # Configuración del navegador
        ruta_chromedriver = "C:/Users/registrolagranja/Documents/PROYECTO ADC/ChromeDriver/chromedriver-win64/chromedriver.exe"
        service = Service(ruta_chromedriver)
        driver = webdriver.Chrome(service=service)

        url = "https://certvigenciacedula.registraduria.gov.co/"
        driver.get(url)

        for _, row in datos.iterrows():
            try:

                # Esperar y hacer clic en el enlace "Expedición Certificado"
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[text()='Expedición Certificado']"))
                ).click()


                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_TextBox1"))
                ).send_keys(str(row["NUMERO DE DOCUMENTO"]))


                # Seleccionar el día en el dropdown
                select_dia = Select(WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList1"))
                ))
                select_dia.select_by_visible_text(str(row["DIA"]))


                # Normalizar el valor del mes (Primera letra mayúscula, resto minúsculas)
                mes_normalizado = str(row["MES"]).capitalize()

                # Seleccionar el mes en el dropdown
                select_mes = Select(WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList2"))
                ))
                select_mes.select_by_visible_text(mes_normalizado)
                

                # Seleccionar el año en el dropdown
                select_ano = Select(WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList3"))
                ))
                select_ano.select_by_visible_text(str(row["AÑO"]))


                # Resolver el captcha LANAP
                captcha_text = driver.find_element(By.ID, "captchaImage").get_attribute("alt")
                if "LANAP" in captcha_text.upper():
                    driver.find_element(By.ID, "txtCaptcha").send_keys("LANAP")

                # Continuar
                driver.find_element(By.ID, "btnContinuar").click()

                # Generar certificado
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "btnGenerarCertificado"))
                ).click()
            except Exception as e:
                print(f"Error al procesar el registro: {e}")
                traceback.print_exc()
                continue

        print("Automatización completada con éxito. Presiona Enter para salir...")
        input()

    except Exception as main_exception:
        print(f"Error general durante la ejecución: {main_exception}")
        traceback.print_exc()

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    archivo_usuario = input("Ingrese el nombre del archivo Excel con los datos: ")
    datos = leer_excel(archivo_usuario)
    if datos is not None:
        automatizar_navegacion(datos)
