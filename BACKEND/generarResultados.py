import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from Plantilla import ajustar_ancho

def generar_resultados(datos, resultados, nombre_archivo_salida="resultados.xlsx"):
    """Genera un archivo Excel de resultados y certificados organizados en carpetas por ficha dentro de Descargas."""
    
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    if not os.path.exists(downloads_folder):
        print("Error: No se puede encontrar la carpeta de descargas.")
        return

    for ficha_numero in datos["FICHA"].unique():
        ficha_str = str(ficha_numero)
        ficha_folder = os.path.join(downloads_folder, ficha_str)

        # Crear la carpeta de la ficha si no existe
        os.makedirs(ficha_folder, exist_ok=True)

        # Guardar el archivo de resultados en la carpeta de la ficha
        datos_ficha = datos[datos["FICHA"] == ficha_numero]
        ruta_archivo_salida = os.path.join(ficha_folder, nombre_archivo_salida)

        try:
            # Guardamos los datos de la ficha en un archivo Excel
            datos_ficha.to_excel(ruta_archivo_salida, index=False, engine="openpyxl")
            ajustar_ancho(ruta_archivo_salida)
        except Exception as e:
            print(f"Error al guardar el archivo Excel para la ficha {ficha_numero}: {e}")
            continue

        try:
            # Cargar el archivo para aplicar colores
            wb = load_workbook(ruta_archivo_salida)
            ws = wb.active

            for idx, row in resultados.iterrows():
                if row["FICHA"] != ficha_numero:
                    continue

                fill_color = None
                if row["STATUS"] == "EXITO":
                    fill_color = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
                elif row["STATUS"] == "NOVEDAD":
                    fill_color = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
                elif row["STATUS"] == "FALLIDO":
                    fill_color = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

                if fill_color:
                    excel_row = idx + 2  # Ajuste por el encabezado
                    for col in range(1, ws.max_column + 1):
                        ws.cell(row=excel_row, column=col).fill = fill_color

            wb.save(ruta_archivo_salida)
            print(f"Archivo de resultados generado y coloreado en: {ruta_archivo_salida}")
        except Exception as e:
            print(f"Error al aplicar colores para la ficha {ficha_numero}: {e}")

        # Generar certificados en la carpeta de la ficha
        for _, row in datos_ficha.iterrows():
            # Nombre del archivo del certificado
            nombre_certificado = f"Certificado_Ficha_{ficha_str}.pdf"
            ruta_certificado = os.path.join(ficha_folder, nombre_certificado)

            # Crear el certificado PDF
            try:
                c = canvas.Canvas(ruta_certificado, pagesize=letter)
                c.setFont("Helvetica", 12)

                # Título del certificado
                c.drawString(200, 750, "Certificado de Participación")

                # Información sobre el aprendiz
                c.drawString(100, 700, f"Nombre: {row['NOMBRES Y APELLIDOS']}")
                c.drawString(100, 675, f"Ficha: {ficha_str}")
                c.drawString(100, 650, f"Estado: {row['STATUS']}")

                # Puedes agregar más detalles aquí si lo necesitas

                # Guardar el archivo PDF
                c.save()
                print(f"Certificado guardado en: {ruta_certificado}")
            except Exception as e:
                print(f"Error al generar el certificado PDF para {row['NOMBRES Y APELLIDOS']}: {e}")
