from typing import Optional

class Proceso:
  id: str
  tamano: int
  tiempo_llegada: int
  tiempo_irrupcion: int
  tiempo_restante:int
  tiempo_finalizacion: Optional[int]
  tiempo_inicio_ejecucion: Optional[int]
  tiempo_total_ejecucion: int
  tiempo_arribo_memoria: Optional[int]

  def __init__(self, id, tamano, tiempo_llegada, tiempo_irrupcion):
    self.id = id
    self.tamano = tamano
    self.tiempo_llegada = tiempo_llegada
    self.tiempo_irrupcion = tiempo_irrupcion
    self.tiempo_restante = tiempo_irrupcion
    self.tiempo_finalizacion = None
    self.tiempo_inicio_ejecucion = None
    self.tiempo_total_ejecucion = 0
    self.tiempo_arribo_memoria = None

  def __repr__(self):
    return f"Proceso(id={self.id}, tamano={self.tamano}, llegada={self.tiempo_llegada}, irrupcion={self.tiempo_irrupcion}, restante={self.tiempo_restante})"

  def actualizar_Estado(self):
    pass

  def calcular_tiempo_espera(self) -> int:
    """Calcula el tiempo de espera como: tiempo_retorno - tiempo_irrupcion
    El tiempo de espera es el tiempo que el proceso no está ejecutándose (en colas)
    Usa tiempo_arribo_memoria como referencia (tiempo al que llega a la cola de Listos)"""
    if self.tiempo_finalizacion is None or self.tiempo_arribo_memoria is None:
      return 0
    tiempo_retorno = self.calcular_tiempo_retorno()
    # El tiempo de espera es el tiempo de retorno menos el tiempo de CPU usado
    # Al finalizar, el tiempo de CPU usado es igual a tiempo_irrupcion
    return tiempo_retorno - self.tiempo_irrupcion

  def calcular_tiempo_retorno(self) -> int:
    """Calcula el tiempo de retorno como: tiempo_finalizacion - tiempo_arribo_memoria
    Usa tiempo_arribo_memoria (tiempo al que llega a la cola de Listos) en lugar de tiempo_llegada"""
    if self.tiempo_finalizacion is None or self.tiempo_arribo_memoria is None:
      return 0
    return self.tiempo_finalizacion - self.tiempo_arribo_memoria
  
  def registrar_inicio_ejecucion(self, tiempo_actual: int):
    """Registra el tiempo en que el proceso comenzó a ejecutarse"""
    if self.tiempo_inicio_ejecucion is None:
      self.tiempo_inicio_ejecucion = tiempo_actual
  
  def registrar_finalizacion(self, tiempo_actual: int):
    """Registra el tiempo en que el proceso finalizó"""
    self.tiempo_finalizacion = tiempo_actual

  def registrar_arribo_memoria(self, tiempo_actual: int):
    """Registra el tiempo en que el proceso llega a la memoria (cola de Listos)"""
    if self.tiempo_arribo_memoria is None:
      self.tiempo_arribo_memoria = tiempo_actual


