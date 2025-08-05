import os
import glob
import PyPDF2
import re

def unir_pdfs(carpeta_destino):
    """
    Une todos los archivos PDF de una carpeta en un solo archivo,
    eliminando duplicados basados en el número de cédula y páginas con contenido insuficiente.
    
    Args:
        carpeta_destino (str): Ruta de la carpeta que contiene los PDFs a unir
    """
    pdf_files = glob.glob(os.path.join(carpeta_destino, "*.pdf"))
    pdf_writer = PyPDF2.PdfWriter()
    cedulas_agregadas = set()
    paginas_eliminadas = 0
    
    for pdf_file in pdf_files:
        with open(pdf_file, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                texto = page.extract_text()
                
                # Verificar si la página tiene contenido suficiente
                if not es_pagina_valida(texto):
                    print(f"Página con contenido insuficiente eliminada del archivo: {os.path.basename(pdf_file)}")
                    paginas_eliminadas += 1
                    continue
                
                # Buscar la cédula en el texto usando regex
                match = re.search(r"Cédula de Ciudadanía:\s+([\d\.]+)", texto)
                if match:
                    cedula = match.group(1).replace('.', '')
                    # Solo añadir si no está repetida
                    if cedula not in cedulas_agregadas:
                        pdf_writer.add_page(page)
                        cedulas_agregadas.add(cedula)
                    else:
                        print(f"Certificado duplicado omitido: {cedula}")
                else:
                    # Si no encuentra cédula pero tiene contenido suficiente, verificar si es página válida
                    if tiene_contenido_certificado(texto):
                        print("Página sin cédula identificable pero con contenido de certificado agregada.")
                        pdf_writer.add_page(page)
                    else:
                        print("Página sin contenido relevante eliminada.")
                        paginas_eliminadas += 1
    
    output_pdf_path = os.path.join(carpeta_destino, "CERTIFICADOS_UNIDOS.pdf")
    with open(output_pdf_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)
    
    print(f"PDF generado sin duplicados: {output_pdf_path}")
    print(f"Total de páginas eliminadas por contenido insuficiente: {paginas_eliminadas}")
    print(f"Total de certificados únicos incluidos: {len(cedulas_agregadas)}")

def es_pagina_valida(texto):
    """
    Verifica si una página tiene contenido suficiente para ser considerada válida.
    
    Args:
        texto (str): Texto extraído de la página PDF
        
    Returns:
        bool: True si la página es válida, False si debe eliminarse
    """
    if not texto or len(texto.strip()) < 50:  # Muy poco texto
        return False
    
    # Verificar que tenga elementos esenciales de un certificado
    elementos_esenciales = [
        "REGISTRADURÍA NACIONAL",
        "CERTIFICA",
        "Cédula de Ciudadanía",
        "Estado:"
    ]
    
    elementos_encontrados = sum(1 for elemento in elementos_esenciales if elemento in texto)
    
    # Debe tener al menos 3 de los 4 elementos esenciales
    if elementos_encontrados < 3:
        return False
    
    # Verificar que no sea solo una página con código de verificación
    lineas = texto.strip().split('\n')
    lineas_con_contenido = [linea for linea in lineas if linea.strip() and len(linea.strip()) > 10]
    
    # Si tiene menos de 5 líneas con contenido real, probablemente es una página vacía
    if len(lineas_con_contenido) < 5:
        return False
    
    return True

def tiene_contenido_certificado(texto):
    """
    Verifica si el texto contiene información relevante de certificado
    aunque no se haya encontrado el patrón de cédula.
    
    Args:
        texto (str): Texto extraído de la página PDF
        
    Returns:
        bool: True si contiene información de certificado
    """
    indicadores_certificado = [
        "REGISTRADURÍA NACIONAL",
        "CERTIFICA",
        "documento de identificación",
        "EDISON QUIÑONES SILVA",
        "Coordinador Grupo Servicio",
        "Para verificar la autenticidad"
    ]
    
    indicadores_encontrados = sum(1 for indicador in indicadores_certificado if indicador in texto)
    
    # Si encuentra al menos 2 indicadores, probablemente es contenido válido
    return indicadores_encontrados >= 2

if __name__ == "__main__":
    # Ejemplo de uso independiente
    carpeta = input("Ingrese la ruta de la carpeta con los PDFs a unir: ")
    if os.path.exists(carpeta):
        unir_pdfs(carpeta)
    else:
        print("La carpeta especificada no existe.")