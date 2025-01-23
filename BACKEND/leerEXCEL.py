import pandas as pd

def leer_excel(archivo_usuario):
    try:
        # Leer el archivo Excel
        datos = pd.read_excel(archivo_usuario, engine='openpyxl')
        if datos.empty:
            print("El archivo no contiene datos. Por favor, verifique el contenido.")
            return None
        else:
            print("Archivo cargado correctamente")
            return datos
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None

if __name__ == "__main__":
    archivo_usuario = input("Ingrese el nombre del archivo Excel con los datos: ")
    datos = leer_excel(archivo_usuario)
