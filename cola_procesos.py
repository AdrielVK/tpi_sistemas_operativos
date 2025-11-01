from proceso import Proceso

class ColaProcesos:
  id: int
  tipo: ["listo", "suspendido", "terminado"]
  procesos: list[Proceso]

  def __init__(self, id, tipo):
    self.id = id
    self.tipo = tipo
    self.procesos = []

  def encolar(self, proceso: Proceso):
    self.procesos.append(proceso)

  def eliminar_proceso(self, proceso: Proceso):
    self.procesos.remove(proceso)

  def ordenar_procesos_por_tiempo_restante(self):
    self.procesos.sort(key=lambda x: x.tiempo_restante)

  def esta_vacio(self)-> bool:
    return len(self.procesos) == 0

  def obtener_primero(self)-> Proceso:
    return self.procesos[0]
