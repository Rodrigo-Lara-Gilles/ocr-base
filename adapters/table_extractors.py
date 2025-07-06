import camelot
from tabulate import tabulate
import logging

def extraer_tablas_pdfplumber(plumber_page):
    """
    Extrae tablas de una página del PDF usando pdfplumber.
    """
    ascii_tables = []
    tbls = plumber_page.extract_tables()
    if tbls:
        for tbl in tbls:
            ascii_tables.append(tabulate(tbl, tablefmt="grid"))
    return ascii_tables

def extraer_tablas_camelot(pdf_path, page_number):
    """
    Extrae tablas de una página del PDF usando Camelot.

    Args:
        pdf_path (str): Ruta al archivo PDF.
        page_number (str or int): Número(s) de página a extraer, como string (por ejemplo, "1" o "1,2,3") o int.
    """
    try:
        tables = camelot.read_pdf(
            pdf_path, pages=str(page_number) if not isinstance(page_number, str) else page_number, flavor="lattice")
        ascii_tables = []
        for t in tables:
            df = t.df
            ascii_table = tabulate(df.values.tolist(), tablefmt="grid")
            ascii_tables.append(ascii_table)
        return ascii_tables
    except Exception as e:
        logging.warning(f"[Camelot] Error on page {page_number}: {e}")
        return []