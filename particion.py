from proceso import Proceso

class Particion:
  id: int
  tamano: int
  direccion_inicio: int
  fragmentacion_interna: int
  procesos: list[Proceso]

  def __init__(self, id, tamano, direccion_inicio, fragmentacion_interna):
    self.id = id
    self.tamano = tamano
    self.direccion_inicio = direccion_inicio
    self.fragmentacion_interna = fragmentacion_interna

  def __str__(self):
    return f"Particion(id={self.id}, tamano={self.tamano}, direccion_inicio={self.direccion_inicio}, fragmentacion_interna={self.fragmentacion_interna})"

  def __repr__(self):
    return self.__str__()

  def esta_libre(self) -> bool:
    pass

  def asignar_proceso(self, proceso: Proceso):
    pass

  def liberar_proceso(self):
    pass

  def calcular_fragmentacion_interna(self) -> int:
    pass
