# Sistema OCR en Contenedor Docker

Este proyecto implementa una solución completa para el procesamiento de documentos PDF, tanto digitales como escaneados. El sistema permite:

- Extraer texto (OCR) con Tesseract
- Detectar y extraer tablas utilizando Camelot y pdfplumber
- Detectar formularios embebidos mediante PyMuPDF
- Indexar el contenido para búsquedas eficientes con Whoosh
- Generar un paquete comprimido con todos los resultados (`.zip`)

La aplicación se ejecuta íntegramente dentro de un contenedor **Docker**, eliminando la necesidad de instalaciones locales complejas.

---

## Requisitos

- Tener [Docker](https://docs.docker.com/get-docker/) instalado (puede complementarse con Colima en sistemas macOS)

---

## Ejecución mediante Docker

1. Clonar el repositorio:

```bash
git clone https://github.com/Rodrigo-Lara-Gilles/ocr-docker-main.git
cd ocr-docker-main
```

2. Crear un archivo `.env` con rutas de volúmenes locales:

```env
HOST_DESKTOP=/Users/tu_usuario/Desktop
HOST_DOWNLOADS=/Users/tu_usuario/Downloads
```

3. Construir e iniciar los servicios:

```bash
docker compose up --build -d
```

4. Iniciar la aplicación de línea de comandos:

```bash
docker exec -it ocr-backend python /app/interfaces/cli/main.py
```

---

## Funcionalidades del menú CLI

| Opción | Funcionalidad                                                   |
|--------|------------------------------------------------------------------|
| **1**  | Procesar un documento PDF desde una URL                         |
| **2**  | Procesar un archivo PDF local desde el escritorio               |
| **3**  | Salir                                                            |

El archivo `resultado.zip` se moverá automáticamente al directorio `~/Downloads`.

---

## Estructura de salida

El sistema genera los siguientes archivos:

- `resultado.json` – Representación estructurada del contenido
- `resultado.txt` – Texto plano con tablas en formato ASCII
- `original.pdf` – Copia del documento original
- `tablas_pag_*.json` – Tablas extraídas por página

---

## Estructura del proyecto

```
backend/
├── adapters/         # Integración con bibliotecas externas (OCR, tablas, indexado)
├── application/      # Casos de uso (descarga, análisis, empaquetado)
├── domain/           # Lógica de negocio central (procesamiento de PDF)
├── interfaces/
│   └── cli/          # Interfaz de línea de comandos
└── resultado/        # Archivos generados tras el procesamiento
```

Cada capa mantiene una dependencia unidireccional hacia las capas inferiores, en concordancia con los principios de *Clean Architecture*.

---

## Cambios recientes

| Fecha       | Descripción de la modificación                                                                  |
|-------------|--------------------------------------------------------------------------------------------------|
| 2025‑07‑05  | Refactorización hacia Clean Architecture (estructura por capas)                                 |
| 2025‑07‑05  | Optimización del Dockerfile utilizando `python:3.11-slim` y separación de dependencias          |
| 2025‑07‑05  | Implementación de CLI desacoplada del núcleo de procesamiento                                   |
| 2025‑07‑05  | Incorporación de variables de entorno para definir rutas locales (`.env`)                       |

---

## Desarrollo y pruebas

- Formateo de código con **black**
- Linting y tipado estático mediante **flake8** y **mypy** (ver `requirements-dev.txt`)
- Ejecución de pruebas unitarias dentro del contenedor:

```bash
docker exec -it ocr-backend pytest
```