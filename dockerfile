# 1. Imagen base liviana
FROM python:3.11-slim

# 2. Configuración para evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# 3. Instalar dependencias del sistema necesarias para OCR, imágenes, PDFs, etc.
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    poppler-utils \
    ghostscript \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libxml2 \
    libxslt1-dev \
    libpoppler-cpp-dev \
    build-essential \
    python3-dev \
    unzip \
    curl \
    zip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# 4. Copiar archivos de requerimientos (producción y desarrollo)
COPY requirements.txt requirements-dev.txt /tmp/

# 5. Instalar pip + dependencias de desarrollo (que incluyen las de prod también)
RUN pip install --upgrade pip && pip install -r /tmp/requirements-dev.txt

# 6. Definir directorio de trabajo dentro del contenedor
WORKDIR /app
ENV PYTHONPATH=/app

# 7. Copiar el código de tu app al contenedor
COPY . /app

# 8. Comando por defecto para iniciar tu app (puede cambiarse si usas gunicorn/uvicorn)
CMD ["python", "interfaces/cli/main.py"]