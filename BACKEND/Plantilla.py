import pandas as pd
from openpyxl import load_workbook

def generar_plantilla():
    # Crear la plantilla
    data = {'TIPO DE DOCUMENTO': [], 'NUMERO DE DOCUMENTO': [], 'NOMBRES Y APELLIDOS': [], 'DIA': [], 'MES': [], 'AÑO': []}
    df = pd.DataFrame(data)
    
    # Guardar la plantilla en un archivo Excel
    nombre_archivo = 'plantilla.xlsx'
    df.to_excel(nombre_archivo, index=False, engine='openpyxl')
    
    # Ajustar el ancho de las columnas
    ajustar_ancho(nombre_archivo)
    print("Se ha generado la plantilla: plantilla.xlsx")

def ajustar_ancho(nombre_archivo):
    # Abrir el archivo Excel para ajustar el ancho de las columnas
    wb = load_workbook(nombre_archivo)
    ws = wb.active

    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter  # Obtener la letra de la columna
        column_name = column[0].value  # Obtener el nombre de la columna
        for cell in column:
            try:
                # Calcular el largo máximo del contenido de la celda
                max_length = max(max_length, len(str(cell.value) if cell.value else ""))
            except Exception as e:
                print(f"Error ajustando ancho: {e}")
        
        # Configurar un ancho específico para la columna "NOMBRE Y APELLIDO"
        if column_name == "NOMBRE  Y APELLIDO":
            adjusted_width = 40  # Ancho específico
        else:
            adjusted_width = max_length + 10  # Ancho calculado dinámicamente
        
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Guardar los cambios en el archivo Excel
    wb.save(nombre_archivo)

if __name__ == "__main__":
    generar_plantilla()
