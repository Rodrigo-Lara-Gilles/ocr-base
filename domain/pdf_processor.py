import os

def procesar_pdf(pdf_path, carpeta_salida):
    # Asegúrate de que estos dos existan y sean rutas válidas
    json_path = os.path.join(carpeta_salida, "salida.json")
    txt_path = os.path.join(carpeta_salida, "salida.txt")
    return json_path, txt_path