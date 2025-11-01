from cola_procesos import ColaProcesosListo, ColaProcesosSuspendido, ColaProcesosTerminado
from cpu import CPU
from proceso import Proceso


class PlanificadorProcesos:
  proceso: Proceso | None
  cola_procesos_listo: ColaProcesosListo
  cola_procesos_suspendido: ColaProcesosSuspendido
  cola_procesos_terminado: ColaProcesosTerminado
  cpu: CPU

  def seleccionar_proximo_proceso(self)-> Proceso:
    return self.cola_procesos.obtener_primero()
  
  def evaluar_preempcion(self)-> bool:
    return self.cpu.get_proceso_actual().tiempo_restante > self.seleccionar_proximo_proceso().tiempo_restante 