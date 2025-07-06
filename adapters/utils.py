import requests
import logging

def descargar_pdf(url, output_file="temp.pdf"):
    """
    Descarga un archivo PDF desde una URL y lo guarda localmente.

    Args:
        url (str): La URL desde la que se descargará el PDF.
        output_file (str, optional): El nombre del archivo donde se guardará el PDF. Por defecto es "temp.pdf".

    Returns:
        raise ValueError(f"Error downloading PDF: {r.status_code}")

    Raises:
        ValueError: Si ocurre un error durante la descarga.
    """
    logging.info(f"Descargando PDF desde: {url}")
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(r.content)
        logging.info("Descarga completada")
        return output_file
    else:
        raise ValueError(f"Error al descargar PDF: {r.status_code}")