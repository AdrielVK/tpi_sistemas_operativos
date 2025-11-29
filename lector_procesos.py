from pathlib import Path
from proceso import Proceso
import sys

class LectorProcesos:
    def __init__(self):

        nombre_archivo = input("Ingrese el nombre del archivo: ") + ".csv"

        # --- Ubicar la carpeta REAL del ejecutable o script ---
        if getattr(sys, 'frozen', False):
            # Ejecutable compilado
            base_dir = Path(sys.executable).parent
        else:
            # Script normal
            base_dir = Path(__file__).parent

        # 1) Buscar en carpeta inputs al lado del ejecutable
        ruta_inputs = base_dir / "inputs" / nombre_archivo

        # 2) Buscar en el mismo directorio que el ejecutable
        ruta_misma_carpeta = base_dir / nombre_archivo

        if ruta_inputs.exists():
            self.ruta_archivo = ruta_inputs
        elif ruta_misma_carpeta.exists():
            self.ruta_archivo = ruta_misma_carpeta
        else:
            raise FileNotFoundError(
                f"No se encontró el archivo en:\n"
                f"- {ruta_inputs}\n"
                f"- {ruta_misma_carpeta}"
            )

    def leer_procesos(self):
        procesos = []
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
                primera_linea = archivo.readline().strip()
                separador = ";" if ";" in primera_linea else ","

                for linea in archivo:
                    if not linea.strip():
                        continue

                    datos = linea.strip().split(separador)

                    if len(datos) != 4:
                        raise ValueError("Formato inválido: se esperaban 4 columnas")

                    id_proceso = str(datos[0])
                    llegada = int(datos[1])
                    tamano = int(datos[2])
                    irrupcion = int(datos[3])

                    proceso = Proceso(
                        id=id_proceso,
                        tamano=tamano,
                        tiempo_llegada=llegada,
                        tiempo_irrupcion=irrupcion,
                    )
                    procesos.append(proceso)

            return procesos

        except Exception as e:
            raise RuntimeError(f"Error al leer el archivo: {e}")
