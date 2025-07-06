import os
from application.use_cases import procesar_desde_url, procesar_desde_archivo
from application.use_cases import ejecutar_ocr
from adapters.utils import descargar_pdf

def menu():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Ingresar URL de PDF")
        print("2. Subir archivo PDF desde el escritorio")
        print("3. Probar con enlace del MOP")
        print("4. Terminar proceso")

        opcion = input("Seleccione una opción (1-4): ").strip()

        if opcion == "1":
            url = input("Ingrese la URL del PDF: ").strip()
            if not url:
                print("No se ingresó una URL válida.")
                continue
            try:
                procesar_desde_url(url)
            except Exception as e:
                print(f"[ERROR]: {e}")

        elif opcion == "2":
            try:
                path = input("Ingrese la ruta del archivo PDF: ").strip()  # <-- Solicitar ruta
                procesar_desde_archivo(path)  # <-- Pasar la ruta como argumento
            except Exception as e:
                print(f"[ERROR]: {e}")

        elif opcion == "3":
            enlace_mop = "https://planeamiento.mop.gob.cl/uploads/sites/12/2025/02/indices_enero_2025-copia.pdf"
            try:
                procesar_desde_url(enlace_mop)
            except Exception as e:
                print(f"[ERROR]: {e}")

        elif opcion == "4":
            print("Proceso finalizado.")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    menu()