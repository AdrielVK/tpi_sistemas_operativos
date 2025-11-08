from proceso import Proceso
from typing import Optional

class Particion:
  id: int
  tamano: int
  direccion_inicio: int
  fragmentacion_interna: int
  proceso: Optional[Proceso]

  def __init__(self, id, tamano, direccion_inicio, fragmentacion_interna):
    self.id = id
    self.tamano = tamano
    self.direccion_inicio = direccion_inicio
    self.fragmentacion_interna = fragmentacion_interna
    self.proceso = None

  def __str__(self):
    if self.proceso:
      return f"Particion(id={self.id}, tamano={self.tamano}, direccion_inicio={self.direccion_inicio}, fragmentacion_interna={self.fragmentacion_interna}, proceso=P{self.proceso.id})"
    else:
      return f"Particion(id={self.id}, tamano={self.tamano}, direccion_inicio={self.direccion_inicio}, fragmentacion_interna={self.fragmentacion_interna}, proceso=LIBRE)"

  def __repr__(self):
    return self.__str__()

  def esta_libre(self) -> bool:
    if self.proceso is None:
      return True
    else:
      return False

  def mostrar_estado(self):
    estado_proceso = f"P{self.proceso.id}" if self.proceso else "LIBRE"
    direccion_fin = self.direccion_inicio + self.tamano - 1
    print(f"  Particion {self.id}: [{self.direccion_inicio:3d}-{direccion_fin:3d}] | Tamaño: {self.tamano:3d} | Estado: {estado_proceso:6s} | Fragmentación interna: {self.fragmentacion_interna:3d}")

  def asignar_proceso(self, proceso: Proceso):
    self.proceso = proceso
    self.fragmentacion_interna = self.tamano - proceso.tamano

  def liberar_proceso(self):
    self.proceso = None
    self.fragmentacion_interna = 0
 
