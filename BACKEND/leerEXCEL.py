import pandas as pd

def validar_plantilla(datos):
    """
    Valida que el archivo Excel tenga la estructura correcta de la plantilla
    
    Args:
        datos (DataFrame): DataFrame con los datos del Excel
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    # Columnas esperadas en la plantilla
    columnas_esperadas = [
        'TIPO DE DOCUMENTO',
        'NUMERO DE DOCUMENTO', 
        'NOMBRES Y APELLIDOS',
        'DIA',
        'MES',
        'AÑO'
    ]
    
    # Verificar que el DataFrame no esté vacío
    if datos.empty:
        return False, "El archivo está vacío. Use la plantilla correcta."
    
    # Obtener las columnas del archivo
    columnas_archivo = list(datos.columns)
    
    # Verificar que tenga el número correcto de columnas
    if len(columnas_archivo) != len(columnas_esperadas):
        return False, f"El archivo debe tener exactamente {len(columnas_esperadas)} columnas. Encontradas: {len(columnas_archivo)}"
    
    # Verificar que las columnas coincidan exactamente
    for i, columna_esperada in enumerate(columnas_esperadas):
        if i >= len(columnas_archivo):
            return False, f"Falta la columna: {columna_esperada}"
        
        columna_actual = str(columnas_archivo[i]).strip()
        if columna_actual != columna_esperada:
            return False, f"Columna incorrecta en posición {i+1}. Esperada: '{columna_esperada}', Encontrada: '{columna_actual}'"
    
    # Validaciones adicionales de contenido
    errores_contenido = []
    
    # Verificar tipos de documento válidos
    tipos_validos = ['CC', 'TI', 'CE', 'PPT']
    for idx, tipo in enumerate(datos['TIPO DE DOCUMENTO'].dropna()):
        if str(tipo).strip().upper() not in tipos_validos:
            errores_contenido.append(f"Fila {idx+2}: Tipo de documento inválido '{tipo}'. Debe ser: {', '.join(tipos_validos)}")
    
    # Verificar que los días sean números válidos
    for idx, dia in enumerate(datos['DIA'].dropna()):
        try:
            dia_num = int(dia)
            if dia_num < 1 or dia_num > 31:
                errores_contenido.append(f"Fila {idx+2}: Día inválido '{dia}'. Debe estar entre 1 y 31")
        except (ValueError, TypeError):
            errores_contenido.append(f"Fila {idx+2}: Día '{dia}' debe ser un número")
    
    # Verificar meses válidos
    meses_validos = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 
                     'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
    for idx, mes in enumerate(datos['MES'].dropna()):
        if str(mes).strip().upper() not in meses_validos:
            errores_contenido.append(f"Fila {idx+2}: Mes inválido '{mes}'. Debe ser uno de: {', '.join(meses_validos)}")
    
    # Verificar años válidos
    año_actual = pd.Timestamp.now().year
    for idx, año in enumerate(datos['AÑO'].dropna()):
        try:
            año_num = int(año)
            if año_num < 1900 or año_num > año_actual:
                errores_contenido.append(f"Fila {idx+2}: Año inválido '{año}'. Debe estar entre 1900 y {año_actual}")
        except (ValueError, TypeError):
            errores_contenido.append(f"Fila {idx+2}: Año '{año}' debe ser un número")
    
    # Si hay errores de contenido, mostrar solo los primeros 5
    if errores_contenido:
        mensaje_errores = "\n".join(errores_contenido[:5])
        if len(errores_contenido) > 5:
            mensaje_errores += f"\n... y {len(errores_contenido) - 5} errores más."
        return False, f"Errores en el contenido del archivo:\n{mensaje_errores}\n\nPor favor, use la plantilla correcta y verifique los datos."
    
    return True, "Plantilla válida"

def leer_excel(archivo_usuario):
    try:
        # Leer el archivo Excel
        datos = pd.read_excel(archivo_usuario, engine='openpyxl')
        
        # Validar la estructura de la plantilla
        es_valido, mensaje = validar_plantilla(datos)
        
        if not es_valido:
            print("ERROR: El archivo no cumple con el formato de la plantilla requerida.")
            print(f"Detalles del error:\n{mensaje}")
            print("\nSolución:")
            print("1. Ejecute el archivo 'Plantilla.py' para generar la plantilla correcta")
            print("2. Use únicamente esa plantilla para ingresar sus datos")
            print("3. No modifique los nombres de las columnas")
            print("4. Respete las validaciones de cada campo")
            return None
        
        if datos.empty:
            print("ADVERTENCIA: El archivo no contiene datos. Por favor, agregue información a la plantilla.")
            return None
        else:
            print("EXITO: Archivo cargado correctamente")
            print(f"INFO: Se encontraron {len(datos)} registros para procesar")
            
            # Mostrar resumen de tipos de documento
            tipos_resumen = datos['TIPO DE DOCUMENTO'].value_counts()
            print("RESUMEN por tipo de documento:")
            for tipo, cantidad in tipos_resumen.items():
                print(f"   - {tipo}: {cantidad} registros")
            
            return datos
            
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo '{archivo_usuario}'")
        print("SOLUCION: Verifique que el archivo existe y está en la ubicación correcta")
        return None
    except Exception as e:
        print(f"ERROR al cargar el archivo: {e}")
        print("VERIFICAR:")
        print("1. El archivo sea un Excel válido (.xlsx)")
        print("2. El archivo no esté abierto en otra aplicación")
        print("3. Use la plantilla generada por 'Plantilla.py'")
        return None

if __name__ == "__main__":
    archivo_usuario = input("Ingrese el nombre del archivo Excel con los datos: ")
    datos = leer_excel(archivo_usuario)
    if datos is not None:
        print("Listo para procesar!")