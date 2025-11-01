class Proceso:
  id: int
  tamano: int
  tiempo_llegada: int
  tiempo_irrupcion: int
  tiempo_restante:int

  def __init__(self, id, tamano, direccion_inicio, fragmentacion_interna):
    self.id = id
    self.tamano = tamano
    self.direccion_inicio = direccion_inicio
    self.fragmentacion_interna = fragmentacion_interna

  def actualizar_Estado(self):
    pass

  def calcular_tiempo_espera(self) -> int:
    pass

  def calcular_tiempo_retorno(self) -> int:
    pass


