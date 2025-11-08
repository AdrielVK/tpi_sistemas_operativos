from proceso import Proceso
from typing import Optional


class CPU:
  proceso: Optional[Proceso]
  def __init__(self):
    self.proceso = None
  
  def __self__(self):
    return f"CPU(proceso={self.proceso})"

  def ejecutar_proceso(self, proceso: Proceso):
    self.proceso = proceso
    #self.proceso.ejecutar()

  def liberar_proceso(self):
    self.proceso = None

  def get_proceso_actual(self)-> Proceso:
    return self.proceso

  def esta_libre(self)-> bool:
    return self.proceso is None