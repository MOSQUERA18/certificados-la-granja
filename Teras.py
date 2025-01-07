from pytesseract import pytesseract, image_to_string
from PIL import Image

# Ruta del ejecutable de Tesseract
pytesseract.tesseract_cmd = r'C:\\Users\\registrolagranja\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

# Cargar una imagen de ejemplo
try:
    image = Image.open('Screenshot_1.png')
    text = image_to_string(image)
    print("Texto detectado:", text)
except Exception as e:
    print("Error:", e)



# import cv2
# import pytesseract
# from PIL import Image
# import numpy as np

# # Ruta al ejecutable de Tesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\registrolagranja\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

# # Cargar la imagen
# image_path = "C:\\certificados-la-granja\\Screenshot_1.png"
# image = cv2.imread(image_path, cv2.IMREAD_COLOR)

# # Convertir a escala de grises
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Aplicar un umbral adaptativo para eliminar las rayas
# thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 4)

# # Invertir colores (texto negro sobre fondo blanco)
# processed_image = cv2.bitwise_not(thresh)

# # Mostrar la imagen procesada (para depuración)
# cv2.imwrite("processed_image.png", processed_image)

# # Realizar OCR en la imagen procesada
# custom_config = r'--oem 3 --psm 6'  # oem 3 para LSTM, psm 6 para texto alineado
# text = pytesseract.image_to_string(processed_image, config=custom_config)
# print("Texto detectado:", text)