# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import Select
# import time
# import traceback
# from leerEXCEL import leer_excel

# def automatizar_navegacion(datos):
#     driver = None
#     try:
#         # Configuración del navegador
#         ruta_chromedriver = "C:\certificados-la-granja\PROYECTO_ADC\ChromeDriver\chromedriver-win64\chromedriver.exe"
#         service = Service(ruta_chromedriver)
#         driver = webdriver.Chrome(service=service)

#         url = "https://certvigenciacedula.registraduria.gov.co/"
#         driver.get(url)

#         for _, row in datos.iterrows():
#             try:

#                 # Esperar y hacer clic en el enlace "Expedición Certificado"
#                 WebDriverWait(driver, 20).until(
#                     EC.element_to_be_clickable((By.XPATH, "//a[text()='Expedición Certificado']"))
#                 ).click()


#                 WebDriverWait(driver, 20).until(
#                     EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_TextBox1"))
#                 ).send_keys(str(row["NUMERO DE DOCUMENTO"]))


#                 # Seleccionar el día en el dropdown
#                 select_dia = Select(WebDriverWait(driver, 20).until(
#                 EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList1"))))
#                 select_dia.select_by_visible_text(str(row["DIA"]).zfill(2))



#                 # Normalizar el valor del mes (Primera letra mayúscula, resto minúsculas)
#                 mes_normalizado = str(row["MES"]).capitalize()

#                 # Seleccionar el mes en el dropdown
#                 select_mes = Select(WebDriverWait(driver, 20).until(
#                     EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList2"))
#                 ))
#                 select_mes.select_by_visible_text(mes_normalizado)
                

#                 # Seleccionar el año en el dropdown
#                 select_ano = Select(WebDriverWait(driver, 20).until(
#                     EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList3"))
#                 ))
#                 select_ano.select_by_visible_text(str(row["AÑO"]))

#                  # Rellenar el campo con el texto "LANAP"
#                 WebDriverWait(driver, 20).until(
#                     EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_TextBox2"))
#                 ).send_keys(str(row["CODIGO"]))


#                 # Resolver el captcha LANAP
#                 captcha_text = driver.find_element(By.ID, "datos_contentplaceholder1_captcha1_CaptchaImage").get_attribute("alt")
#                 if "LANAP" in captcha_text.upper():
#                     driver.find_element(By.ID, "datos_contentplaceholder1_captcha1_CaptchaImage").send_keys("LANAP")
#                      # Rellenar el campo con el texto "LANAP"
#                     WebDriverWait(driver, 20).until(
#                     EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_TextBox2"))
#                     ).send_keys(str(row["CODIGO"]))

#                 # Continuar
#                 driver.find_element(By.ID, "ContentPlaceHolder1_Button1").click()

#                 # Generar certificado
#                 WebDriverWait(driver, 20).until(
#                     EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_Button1"))
#                 ).click()


#                 # CLICK PARA VOLVER A LA PAGINA PRINCIPAL
#                 WebDriverWait(driver, 20).until(
#                     EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_LinkButton1"))
#                 ).click()
#             except Exception as e:
#                 print(f"Error al procesar el registro: {e}")
#                 traceback.print_exc()
#                 continue

#         print("Automatización completada con éxito. Presiona Enter para salir...")
#         input()

#     except Exception as main_exception:
#         print(f"Error general durante la ejecución: {main_exception}")
#         traceback.print_exc()

#     finally:
#         if driver:
#             driver.quit()

# if __name__ == "__main__":
#     archivo_usuario = input("Ingrese el nombre del archivo Excel con los datos: ")
#     datos = leer_excel(archivo_usuario)
#     if datos is not None:
#         automatizar_navegacion(datos)



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import traceback
from leerEXCEL import leer_excel
from selenium.common.exceptions import UnexpectedAlertPresentException

def automatizar_navegacion(datos):
    driver = None
    try:
        # Configuración del navegador
        ruta_chromedriver = "C:\\certificados-la-granja\\PROYECTO_ADC\\ChromeDriver\\chromedriver-win64\\chromedriver.exe"
        service = Service(ruta_chromedriver)
        driver = webdriver.Chrome(service=service)

        url = "https://certvigenciacedula.registraduria.gov.co/"
        driver.get(url)

        for _, row in datos.iterrows():
            try:
                # Ir a la página principal en cada iteración
                driver.get(url)

                # Hacer clic en "Expedición Certificado"
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[text()='Expedición Certificado']"))
                ).click()

                # Llenar número de documento
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_TextBox1"))
                ).send_keys(str(row["NUMERO DE DOCUMENTO"]))

                # Seleccionar día
                select_dia = Select(WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList1"))
                ))
                select_dia.select_by_visible_text(str(row["DIA"]).zfill(2))

                # Normalizar el valor del mes
                mes_normalizado = str(row["MES"]).capitalize()

                # Seleccionar mes
                select_mes = Select(WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList2"))
                ))
                select_mes.select_by_visible_text(mes_normalizado)

                # Seleccionar año
                select_ano = Select(WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_DropDownList3"))
                ))
                select_ano.select_by_visible_text(str(row["AÑO"]))

                # Rellenar el campo del CAPTCHA
                campo_captcha = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_TextBox2"))
                )
                campo_captcha.clear()
                campo_captcha.send_keys("LANAP")

                # Resolver el CAPTCHA manualmente (espera a que el usuario lo valide)
                captcha_resuelto = False
                while not captcha_resuelto:
                    try:
                        # Intentar hacer clic en el botón de continuar
                        boton_continuar = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_Button1"))
                        )
                        boton_continuar.click()

                        # Verificar si se genera una alerta por CAPTCHA incorrecto
                        WebDriverWait(driver, 5).until(EC.alert_is_present())
                        alerta = driver.switch_to.alert
                        print("Alerta detectada: CAPTCHA incorrecto")
                        alerta.accept()  # Cerrar la alerta

                        # Volver a escribir el CAPTCHA
                        campo_captcha.clear()
                        campo_captcha.send_keys("LANAP")

                    except UnexpectedAlertPresentException:
                        print("Se presentó una alerta inesperada. Volviendo a intentar...")
                        continue
                    except Exception:
                        # Si no hay alerta, asumimos que el CAPTCHA fue correcto
                        captcha_resuelto = True

                #Generar certificado
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_Button1"))
                ).click()

                # Regresar a la página principal
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_LinkButton1"))
                ).click()
                print("Certificado generado correctamente. Procediendo con la siguiente fila...")

            except Exception as e:
                print(f"Error al procesar el registro: {e}")
                traceback.print_exc()
                continue

        print("Automatización completada con éxito.")
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
