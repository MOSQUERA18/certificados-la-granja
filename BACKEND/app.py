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

logging.basicConfig(level=logging.DEBUG)

# Agrega esta variable al inicio de tu archivo app.py
archivo_generado = False

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde React

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear carpeta si no existe

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
    filepath = os.path.join(UPLOAD_FOLDER, "archivo_subido.xlsx")

    if not os.path.exists(filepath):
        return jsonify({"error": "No hay archivo subido"}), 400

    datos = leer_excel(filepath)  
    if datos is None:
        return jsonify({"error": "No hay datos para procesar"}), 400
    
    automatizar_navegacion(datos)
    return jsonify({"mensaje": "Automatización iniciada"}), 200

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
    archivo_resultados = "resultados_certificados.xlsx"  # Asegúrate de que este archivo se genere correctamente

    if not os.path.exists(archivo_resultados):
        return jsonify({"error": "El archivo no está disponible."}), 404

    return send_file(archivo_resultados, as_attachment=True)

if __name__ == '__main__':
    logging.info("Servidor iniciado en http://127.0.0.1:50400")
    serve(app, host="0.0.0.0", port=5000)
