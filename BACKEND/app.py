import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os
from leerEXCEL import leer_excel
from navegacion import automatizar_navegacion
from Plantilla import generar_plantilla
from waitress import serve
import logging
from pathlib import Path
from generarResultados import generar_resultados 

# Desactivar logs de Flask y Waitress
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('waitress').setLevel(logging.ERROR)

# Configurar logging solo para errores críticos
logging.basicConfig(level=logging.ERROR)

# Desactivar logs de pandas y otros módulos comunes
logging.getLogger('pandas').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('selenium').setLevel(logging.ERROR)

# Agrega esta variable al inicio de tu archivo app.py
ruta_carpeta_descargas = None

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde React

# Desactivar logs internos de Flask
app.logger.disabled = True
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear carpeta si no existe

@app.route('/crear-carpeta-descargas', methods=['POST'])
def crear_carpeta_en_descargas():
    global ruta_carpeta_descargas  # usamos la variable global
    try:
        data = request.get_json()
        nombre_carpeta = data.get('nombre')
        if not nombre_carpeta:
            return jsonify({"error": "No se proporcionó un nombre de carpeta"}), 400
        carpeta_descargas = str(Path.home() / "Downloads")
        ruta_carpeta = os.path.join(carpeta_descargas, nombre_carpeta)
        os.makedirs(ruta_carpeta, exist_ok=True)
        ruta_carpeta_descargas = ruta_carpeta  # Guardar la ruta
        return jsonify({"mensaje": f"Carpeta creada en: {ruta_carpeta}"}), 200
    except Exception as e:
        return jsonify({"error": f"No se pudo crear la carpeta: {str(e)}"}), 500

@app.route('/')
def home():
    return jsonify({"mensaje": "Servidor Flask funcionando correctamente"}), 200

@app.route('/subir-excel', methods=['POST'])
def subir_excel():
    if 'file' not in request.files:
        return jsonify({"error": "No se envió ningún archivo"}), 400
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, "archivo_subido.xlsx")
    file.save(filepath)  # Guardar archivo con nombre fijo
    return jsonify({"mensaje": "Archivo recibido correctamente"}), 200

@app.route('/iniciar-automatizacion', methods=['POST'])
def iniciar_automatizacion():
    global ruta_carpeta_descargas
    filepath = os.path.join(UPLOAD_FOLDER, "archivo_subido.xlsx")
    if not os.path.exists(filepath):
        return jsonify({"error": "No hay archivo subido"}), 400
    
    datos = leer_excel(filepath)  
    
    if datos is None:
        return jsonify({"error": "No hay datos para procesar"}), 400
    
    # Aquí deberías obtener el DataFrame de resultados
    resultados = automatizar_navegacion(datos, carpeta_destino=ruta_carpeta_descargas)
    
    # Y ahora llamas a la función pasando la ruta
    generar_resultados(datos, resultados, nombre_archivo_salida="resultados_certificados.xlsx", carpeta_destino=ruta_carpeta_descargas)
    
    return jsonify({"mensaje": "Automatización finalizada y resultados guardados"}), 200

@app.route('/descargar-plantilla', methods=['GET'])
def descargar_plantilla():
    try:
        generar_plantilla()  # Generar la plantilla antes de enviarla
        
        # Leer el archivo y convertirlo a base64
        with open("plantilla.xlsx", "rb") as file:
            base64_data = base64.b64encode(file.read()).decode('utf-8')
        
        return jsonify({"archivo_base64": base64_data, "nombre": "plantilla.xlsx"})
        
    except Exception as e:
        return jsonify({"error": f"Error al descargar: {str(e)}"}), 500

@app.route('/descargar-resultados', methods=['GET'])
def descargar_resultados():
    global ruta_carpeta_descargas
    if not ruta_carpeta_descargas:
        return jsonify({"error": "La carpeta de descarga no ha sido definida."}), 400
    
    archivo_resultados = os.path.join(ruta_carpeta_descargas, "resultados_certificados.xlsx")
    if not os.path.exists(archivo_resultados):
        return jsonify({"error": "El archivo no está disponible."}), 404
    
    return send_file(archivo_resultados, as_attachment=True)

if __name__ == '__main__':
    # Solo un mensaje inicial mínimo
    print("Servidor iniciado en http://0.0.0.0:5000")
    serve(app, host="0.0.0.0", port=5000)