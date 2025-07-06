import os
import shutil
import requests
import subprocess
import tempfile
from domain.pdf_processor import procesar_pdf 

# Prefijos de ruta configurables, ahora solo leídos desde variables de entorno (.env)
HOST_PATH_PREFIX = os.getenv("HOST_PATH_PREFIX")
CONTAINER_PATH_PREFIX = os.getenv("CONTAINER_PATH_PREFIX")

def ejecutar_ocr(path_pdf, carpeta_resultado):
    """
    Ejecuta el procesamiento OCR sobre un PDF dado y guarda los resultados en la carpeta especificada.
    """
    return procesar_pdf(path_pdf, carpeta_resultado)

def procesar_desde_url(url):
    """
    Descarga un PDF desde una URL, lo guarda temporalmente y procesa el archivo descargado.
    Los resultados se guardan en la carpeta 'resultado'.
    """
    pdf_path = "temp.pdf"
    carpeta_salida = "resultado"
    # Asegura que la carpeta de salida exista
    os.makedirs(carpeta_salida, exist_ok=True)
    # Descarga el PDF desde la URL proporcionada
    descargar_pdf(url, pdf_path)
    # Procesa el PDF descargado y genera los resultados
    generar_resultados(pdf_path, carpeta_salida)

def procesar_desde_archivo(path, carpeta_salida="resultado"):
    """
    Procesa un archivo PDF desde una ruta proporcionada por el usuario.
    Realiza la conversión de la ruta de la máquina anfitriona a la ruta del contenedor si es necesario,
    verifica la existencia del archivo, y luego procesa el PDF.
    """
    print(f"DEBUG: Ruta ingresada: {path}")

    # Si la ruta comienza con el prefijo de la máquina anfitriona, la convierte al prefijo del contenedor
    if path.startswith(HOST_PATH_PREFIX):
        path = path.replace(HOST_PATH_PREFIX, CONTAINER_PATH_PREFIX)
    print(f"DEBUG: Ruta convertida: {path}")

    # Verifica si el archivo existe en la ruta convertida
    if not os.path.isfile(path):
        print("No se encontró el archivo especificado.")
        return  # O alternativamente: raise FileNotFoundError("No se encontró el archivo especificado.")

    # Crea un archivo temporal para copiar el PDF y procesarlo
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        temp_path = tmp_file.name
    shutil.copy(path, temp_path)
    # Procesa el archivo temporal y genera los resultados
    generar_resultados(temp_path, carpeta_salida)
    # Elimina el archivo temporal después de procesar
    os.remove(temp_path)
    # (Código duplicado, probablemente innecesario)
    os.makedirs(carpeta_salida, exist_ok=True)
    temp_path = "temp.pdf"
    shutil.copy(path, temp_path)
    generar_resultados(temp_path, carpeta_salida)

def generar_resultados(pdf_path, carpeta_salida):
    """
    Procesa el PDF usando OCR, copia el PDF original a la carpeta de salida,
    y empaqueta los resultados (JSON, TXT y PDF) en un archivo ZIP que se mueve a la carpeta Descargas del usuario.
    """
    # Procesa el PDF y obtiene las rutas de los archivos de salida (JSON y TXT)
    json_path, txt_path = procesar_pdf(pdf_path, carpeta_salida)
    # Copia el PDF original a la carpeta de salida
    pdf_output = os.path.join(carpeta_salida, "original.pdf")
    shutil.copy(pdf_path, pdf_output)
    # Crea un archivo ZIP con los resultados
    subprocess.run(["zip", "-j", "resultado.zip", json_path, txt_path, pdf_output], check=True)
    
    # (Código redundante: vuelve a crear el ZIP solo con el JSON)
    import zipfile
    zip_filename = "resultado.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(json_path, os.path.basename(json_path))
    # Define la ruta de destino final del ZIP en la carpeta Descargas del usuario
    destino = os.path.expanduser("~/Downloads/resultado.zip")
    os.makedirs(os.path.dirname(destino), exist_ok=True)  # Crea la carpeta si no existe
    if os.path.exists(destino):
        os.remove(destino)
    # Mueve el ZIP generado a la carpeta Descargas
    shutil.move("resultado.zip", destino)
    print(f"Proceso completado. ZIP guardado en: {destino}")

def descargar_pdf(url, output_path):
    """
    Descarga un archivo PDF desde una URL y lo guarda en la ruta especificada.
    Maneja errores de conexión y verifica el código de estado de la respuesta.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"PDF descargado correctamente en {output_path}")
        else:
            print(f"Error al descargar el PDF. Código de estado: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el PDF: {e}")