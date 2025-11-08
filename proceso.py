class Proceso:
  id: int
  tamano: int
  tiempo_llegada: int
  tiempo_irrupcion: int
  tiempo_restante:int
  tiempo_finalizacion: int | None
  tiempo_inicio_ejecucion: int | None
  tiempo_total_ejecucion: int

  def __init__(self, id, tamano, tiempo_llegada, tiempo_irrupcion):
    self.id = id
    self.tamano = tamano
    self.tiempo_llegada = tiempo_llegada
    self.tiempo_irrupcion = tiempo_irrupcion
    self.tiempo_restante = tiempo_irrupcion
    self.tiempo_finalizacion = None
    self.tiempo_inicio_ejecucion = None
    self.tiempo_total_ejecucion = 0

  def __repr__(self):
    return f"Proceso(id={self.id}, tamano={self.tamano}, llegada={self.tiempo_llegada}, irrupcion={self.tiempo_irrupcion}, restante={self.tiempo_restante})"

  def actualizar_Estado(self):
    pass

  def calcular_tiempo_espera(self) -> int:
    """Calcula el tiempo de espera como: tiempo_retorno - tiempo_irrupcion"""
    if self.tiempo_finalizacion is None:
      return 0
    tiempo_retorno = self.calcular_tiempo_retorno()
    return tiempo_retorno - self.tiempo_irrupcion

  def calcular_tiempo_retorno(self) -> int:
    """Calcula el tiempo de retorno como: tiempo_finalizacion - tiempo_llegada"""
    if self.tiempo_finalizacion is None:
      return 0
    return self.tiempo_finalizacion - self.tiempo_llegada
  
  def registrar_inicio_ejecucion(self, tiempo_actual: int):
    """Registra el tiempo en que el proceso comenzó a ejecutarse"""
    if self.tiempo_inicio_ejecucion is None:
      self.tiempo_inicio_ejecucion = tiempo_actual
  
  def registrar_finalizacion(self, tiempo_actual: int):
    """Registra el tiempo en que el proceso finalizó"""
    self.tiempo_finalizacion = tiempo_actual


