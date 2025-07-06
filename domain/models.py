from typing import Any, Dict, List

class PaginaProcesada:
    """
    Representa una página procesada por OCR.

    Attributes:
        numero (int): Número de la página.
        texto (str): Texto extraído de la página.
        ocr (str): Motor OCR utilizado.
        precision (float): Precisión del OCR.
        tablas (list): Lista de tablas detectadas en la página.
    """
    def __init__(self, numero, texto, ocr, precision, tablas=None):
        # Use tablas=None to avoid mutable default argument issues; assign empty list if None
        self.numero = numero
        self.texto = texto
        self.ocr = ocr
        self.precision = precision
        self.tablas = tablas or []

class ResultadoOCR:
    def __init__(
        self,
        archivo: str,
        metadata: Dict[str, Any],
        estadisticas: Dict[str, Any],
        paginas: List[PaginaProcesada],
        formularios: List[Any]
    ):
        self.archivo = archivo
        self.metadata = metadata
        self.paginas = paginas
        self.formularios = formularios
        self.formularios = formularios