from cola_procesos import ColaProcesosListo, ColaProcesosListoSuspendido, ColaProcesosSuspendido, ColaProcesosTerminado
from cpu import CPU
from proceso import Proceso
from typing import Optional


class PlanificadorProcesos:
  proceso_entrante: Optional[Proceso]
  cpu: CPU
  cola_procesos_listo: ColaProcesosListo
  cola_procesos_suspendido: ColaProcesosSuspendido
  cola_procesos_terminado: ColaProcesosTerminado
  cola_listo_suspendido: ColaProcesosListoSuspendido

  def __init__(self,cola_listo_suspendido:ColaProcesosListoSuspendido,cpu: CPU, cola_procesos_listo:ColaProcesosListo, cola_procesos_suspendido:ColaProcesosSuspendido, cola_procesos_terminado:ColaProcesosTerminado):
    self.proceso_entrante=None
    self.cola_procesos_listo=cola_procesos_listo
    self.cola_procesos_suspendido=cola_procesos_suspendido
    self.cola_procesos_terminado=cola_procesos_terminado
    self.cola_listo_suspendido=cola_listo_suspendido
    self.cpu = cpu
    
  
  def ejecutar_preempcion(self, proceso_nuevo: Proceso):
    """Ejecuta la preempción: saca el proceso actual de CPU y pone el nuevo"""
    proceso_actual = self.cpu.get_proceso_actual()
    if proceso_actual:
      # El proceso actual debe volver a la cola de listo
      # Primero eliminarlo si ya está (para evitar duplicados) y luego agregarlo
      if proceso_actual in self.cola_procesos_listo.procesos:
        self.cola_procesos_listo.eliminar_proceso(proceso_actual)
      self.cola_procesos_listo.encolar(proceso_actual)
    
    # Eliminar el proceso nuevo de la cola si está ahí (porque va a CPU)
    if proceso_nuevo in self.cola_procesos_listo.procesos:
      self.cola_procesos_listo.eliminar_proceso(proceso_nuevo)
    
    # Asignar el nuevo proceso a la CPU
    self.cpu.ejecutar_proceso(proceso_nuevo)
    return proceso_actual  # Retornar el proceso preemptado para informar

  def evaluar_preempcion(self, proceso: Proceso)-> bool:
    proceso_actual = self.cpu.get_proceso_actual()
    if proceso_actual and proceso_actual.tiempo_restante > proceso.tiempo_restante:
      return True
    else:
      return False
  
  def planificar_proceso_entrante(self, proceso: Proceso) -> Optional[Proceso]:
    """
    Planifica un proceso entrante. Retorna el proceso preemptado si hubo preempción, None en caso contrario.
    """
    if self.cpu.esta_libre():
      # Eliminar el proceso de la cola si está ahí (va a CPU)
      if proceso in self.cola_procesos_listo.procesos:
        self.cola_procesos_listo.eliminar_proceso(proceso)
      self.cpu.ejecutar_proceso(proceso)
      return None
    elif self.evaluar_preempcion(proceso):
      proceso_preemptado = self.ejecutar_preempcion(proceso)
      return proceso_preemptado
    else:
      # El proceso no se puede ejecutar ahora, se queda en la cola de listo
      # Asegurar que esté en la cola
      if proceso not in self.cola_procesos_listo.procesos:
        self.cola_procesos_listo.encolar(proceso)
      return None