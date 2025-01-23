import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from Plantilla import ajustar_ancho  # Importar la función para ajustar ancho de columnas

def generar_resultados(datos, resultados, nombre_archivo_salida="resultados.xlsx"):
    if datos.empty:
        print("Error: El DataFrame 'datos' está vacío. No se puede generar el archivo.")
        return
    if resultados.empty:
        print("Error: El DataFrame 'resultados' está vacío. No se puede generar el archivo.")
        return

    # Agregar la columna de observaciones al DataFrame original
    print("Agregando columna de observaciones...")
    datos["OBSERVACIONES"] = resultados["OBSERVACIONES"]

    # Guardar el archivo Excel con las observaciones
    try:
        datos.to_excel(nombre_archivo_salida, index=False, engine="openpyxl")
        print(f"Archivo guardado como: {nombre_archivo_salida}")
    except Exception as e:
        print(f"Error al guardar el archivo Excel: {e}")
        return

    # Ajustar el ancho de las columnas según el formato de la plantilla
    try:
        ajustar_ancho(nombre_archivo_salida)
    except Exception as e:
        print(f"Error al ajustar el ancho de las columnas: {e}")
        return

    # Cargar el archivo Excel para aplicar colores
    try:
        wb = load_workbook(nombre_archivo_salida)
        ws = wb.active

        # Aplicar colores a las filas según el estado
        for idx, row in resultados.iterrows():
            fill_color = None

            # Verificar si la fila contiene datos válidos
            if pd.isna(row.get("STATUS")) or pd.isna(row.get("OBSERVACIONES")):
                continue  # Saltar filas sin datos

            if row["STATUS"] == "EXITO":
                fill_color = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")  # Verde
            elif row["STATUS"] == "FALLIDO":
                fill_color = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")  # Rojo

            if fill_color:
                excel_row = idx + 2  # Compensar por el encabezado
                for col in range(1, ws.max_column + 1):
                    ws.cell(row=excel_row, column=col).fill = fill_color

        # Guardar los cambios
        wb.save(nombre_archivo_salida)
        print(f"Archivo de resultados generado y coloreado: {nombre_archivo_salida}")
    except Exception as e:
        print(f"Error al aplicar colores: {e}")

