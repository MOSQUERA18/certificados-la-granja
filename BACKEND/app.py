from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from leerEXCEL import leer_excel
from navegacion import automatizar_navegacion

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde React

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear carpeta si no existe

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Cambia el puerto a 5000 para evitar conflictos con React
