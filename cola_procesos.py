from proceso import Proceso
from abc import ABC
from typing import List

class ColaProcesos(ABC):
  id: int
  tipo = ["listo", "suspendido", "terminado", "listo_suspendido", "nuevo"]
  procesos: List[Proceso]

  def __init__(self, id, tipo):
    self.id = id
    self.tipo = tipo
    self.procesos = []

  def encolar(self, proceso: Proceso):
    self.procesos.append(proceso)

  def eliminar_proceso(self, proceso: Proceso):
    """Elimina un proceso de la cola si está presente"""
    if proceso in self.procesos:
      self.procesos.remove(proceso)

  def esta_vacio(self)-> bool:
    return len(self.procesos) == 0

  def obtener_primero_por_tiempo(self)-> Proceso:
    self.procesos.sort(key=lambda x: x.tiempo_restante)
    return self.procesos[0]

class ColaProcesosListo(ColaProcesos):
  def __init__(self):
    super().__init__(1, "listo")


class ColaProcesosTerminado(ColaProcesos):
  def __init__(self):
    super().__init__(3, "terminado")

class ColaProcesosListoSuspendido(ColaProcesos):
  def __init__(self):
    super().__init__(4, "listo_suspendido")

class ColaProcesosSuspendido(ColaProcesos):
  def __init__(self):
    super().__init__(2, "suspendido")

class ColaProcesosNuevos(ColaProcesos):
  def __init__(self):
    super().__init__(4, "nuevo")
  
  def get_procesos_by_tiempo_llegada(self, valor_reloj_global:int):
    result = []
    procesos_restantes = []
    for proceso in self.procesos:
      if proceso.tiempo_llegada == valor_reloj_global:
        result.append(proceso)
      else:
        procesos_restantes.append(proceso)
    self.procesos = procesos_restantes
    return result
    