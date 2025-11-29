from pathlib import Path
from proceso import Proceso

class LectorProcesos:
  def __init__(self):
    nombre_archivo = input("Ingrese el nombre del archivo: ")
    # Obtener la ruta base (carpeta donde se ejecuta el main)
    #base_dir = Path(__file__).resolve().parent.parent  # sube desde /simulador hacia /ProyectoSO
    base_dir=Path.cwd()
    self.ruta_archivo = base_dir/"inputs"/f"{nombre_archivo}.csv"

  def leer_procesos(self):
    procesos = []
    try:
      with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
        primera_linea = archivo.readline().strip()           
        separador = ";" if ";" in primera_linea else ","
        encabezado = primera_linea.split(separador)
        for linea in archivo:
          datos = linea.strip().split(separador)
          # Ignorar líneas vacías
          if not linea.strip():
            continue
          print(datos)
          if len(datos) != 4:
            raise ValueError("Formato inválido de línea: se esperaban 4 columnas")

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
      #procesos.sort(key=lambda p: p.tiempo_llegada)
      return procesos

    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {self.ruta_archivo}")
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo: {e}")
