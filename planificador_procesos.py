from cola_procesos import ColaProcesosListo, ColaProcesosListoSuspendido, ColaProcesosSuspendido, ColaProcesosTerminado
from cpu import CPU
from proceso import Proceso


class PlanificadorProcesos:
  proceso_entrante: Proceso | None
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
    
  
  def ejecutar_preempcion(self, proceso_nuevo):
    self.cpu.ejecutar_proceso(proceso_nuevo)

  def evaluar_preempcion(self, proceso: Proceso)-> bool:
    if self.cpu.get_proceso_actual().tiempo_restante > proceso.tiempo_restante:
      return True
    else:
      return False
  
  def planificar_proceso_entrante(self, proceso):
    if self.cpu.esta_libre():
      self.cpu.ejecutar_proceso(proceso)
    elif self.evaluar_preempcion(proceso):
      self.ejecutar_preempcion()
      #queda en la lista de listo (dentro de la memoria)