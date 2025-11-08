from calendar import c
from cola_procesos import ColaProcesosListo, ColaProcesosListoSuspendido, ColaProcesosNuevos, ColaProcesosSuspendido, ColaProcesosTerminado
from cpu import CPU
from lector_procesos import LectorProcesos
from memoria import Memoria
from planificador_procesos import PlanificadorProcesos


class Simulador:
  memoria: Memoria
  planificador_procesos: PlanificadorProcesos
  cpu: CPU
  cola_listo: ColaProcesosListo
  cola_terminado: ColaProcesosTerminado
  cola_listo_suspendido: ColaProcesosListoSuspendido
  cola_procesos_nuevos: ColaProcesosNuevos
  lector_procesos: LectorProcesos
  reloj_global: int
  grado_multiprogramacion = 5
  length_procesos_nuevos: int

  def __init__(self):
    self.memoria = Memoria()
    self.cola_listo = ColaProcesosListo()
    self.cola_terminado = ColaProcesosTerminado()
    self.cola_listo_suspendido = ColaProcesosListoSuspendido()
    self.cola_procesos_nuevos = ColaProcesosNuevos()
    self.lector_procesos = LectorProcesos()
    self.cpu = CPU()
    # Crear cola_suspendido si no existe (se usa pero no está definida)
    self.cola_suspendido = ColaProcesosListoSuspendido()  # Usando la misma para simplificar
    self.planificador_procesos = PlanificadorProcesos(
      cola_listo_suspendido=self.cola_listo_suspendido,
      cola_procesos_listo=self.cola_listo,
      cola_procesos_terminado=self.cola_terminado,
      cola_procesos_suspendido=self.cola_suspendido,
      cpu = self.cpu
      )
    self.reloj_global = 0
    self.length_procesos_nuevos = 0

  
  def check_multiprogramacion(self) -> bool:
    if (len(self.cola_listo_suspendido.procesos) + len(self.cola_listo.procesos)) >= self.grado_multiprogramacion:
      return True
    return False
  
  def evento_llegada(self):
    return self.cola_procesos_nuevos.get_procesos_by_tiempo_llegada(valor_reloj_global=self.reloj_global)


  def generar_informes(self):
    """Genera un informe estadístico con tiempos de retorno, espera y rendimiento del sistema"""
    print("\n" + "="*80)
    print("INFORME ESTADÍSTICO DE LA SIMULACIÓN")
    print("="*80)
    
    procesos_terminados = self.cola_terminado.procesos
    
    if not procesos_terminados:
      print("No hay procesos terminados para generar el informe.")
      return
    
    # Calcular estadísticas para cada proceso
    tiempos_retorno = []
    tiempos_espera = []
    
    print("\n" + "-"*80)
    print(f"{'Proceso':<10} {'Tiempo Llegada':<18} {'Tiempo Finalización':<22} {'Tiempo Retorno':<18} {'Tiempo Espera':<15}")
    print("-"*80)
    
    for proceso in procesos_terminados:
      tiempo_retorno = proceso.calcular_tiempo_retorno()
      tiempo_espera = proceso.calcular_tiempo_espera()
      
      tiempos_retorno.append(tiempo_retorno)
      tiempos_espera.append(tiempo_espera)
      
      print(f"P{proceso.id:<9} {proceso.tiempo_llegada:<18} {proceso.tiempo_finalizacion:<22} {tiempo_retorno:<18} {tiempo_espera:<15}")
    
    # Calcular promedios
    tiempo_retorno_promedio = sum(tiempos_retorno) / len(tiempos_retorno) if tiempos_retorno else 0
    tiempo_espera_promedio = sum(tiempos_espera) / len(tiempos_espera) if tiempos_espera else 0
    
    print("-"*80)
    print(f"{'PROMEDIO':<10} {'':<18} {'':<22} {tiempo_retorno_promedio:<18.2f} {tiempo_espera_promedio:<15.2f}")
    print("-"*80)
    
    # Calcular rendimiento del sistema
    cantidad_procesos_terminados = len(procesos_terminados)
    tiempo_total_simulacion = self.reloj_global
    rendimiento = cantidad_procesos_terminados / tiempo_total_simulacion if tiempo_total_simulacion > 0 else 0
    
    print("\n" + "="*80)
    print("ESTADÍSTICAS GENERALES")
    print("="*80)
    print(f"Cantidad de procesos terminados: {cantidad_procesos_terminados}")
    print(f"Tiempo total de simulación: {tiempo_total_simulacion} unidades de tiempo")
    print(f"Rendimiento del sistema: {rendimiento:.4f} procesos/unidad de tiempo")
    print(f"Tiempo promedio de retorno: {tiempo_retorno_promedio:.2f} unidades de tiempo")
    print(f"Tiempo promedio de espera: {tiempo_espera_promedio:.2f} unidades de tiempo")
    print("="*80 + "\n")

  def planificar_proceso(self, proceso):
    proceso_preemptado = self.planificador_procesos.planificar_proceso_entrante(proceso)
    
    # Si hubo preempción, informar
    if proceso_preemptado:
      print(f"\n>>> PREEMPCIÓN: Proceso P{proceso.id} (tiempo restante: {proceso.tiempo_restante}) preempta a P{proceso_preemptado.id} (tiempo restante: {proceso_preemptado.tiempo_restante})")
      print(f"    Proceso P{proceso_preemptado.id} vuelve a la cola de listo")
      # El proceso preemptado ya fue agregado a la cola en ejecutar_preempcion()
      # Mostrar estado de memoria después de la preempción
      self.memoria.mostrar_estados(tipo_evento=f"preempción: P{proceso.id} preempta a P{proceso_preemptado.id}")
    
    # Registrar inicio de ejecución cuando el proceso realmente se asigna a la CPU
    if self.cpu.proceso == proceso and proceso.tiempo_inicio_ejecucion is None:
      proceso.registrar_inicio_ejecucion(self.reloj_global)

  def agregar_proceso_cola_suspendido(self, proceso):
    self.cola_suspendido.encolar(proceso)

  def actualizar_cola_listo(self, proceso):
    self.cola_listo.encolar(proceso)
    

  def reubicar_procesos_suspendidos(self):
    p_suspendidos = self.cola_listo_suspendido.procesos.copy()
    self.cola_listo_suspendido.procesos.clear()
    for p in p_suspendidos:
      if not self.check_multiprogramacion():
        particion = self.memoria.buscar_particion_best_fit(p)
        if particion:
          print(f"    Reubicando proceso suspendido P{p.id} a partición {particion.id}")
          particion.asignar_proceso(p)
          self.actualizar_cola_listo(p)
          self.planificar_proceso(p)
          self.memoria.mostrar_estados(tipo_evento=f"reubicación proceso P{p.id} suspendido")
        else:
          self.cola_listo_suspendido.encolar(p)
      else:
        self.cola_listo_suspendido.encolar(p)

  def procesar_llegadas(self):
    lista_procesos_entrantes = self.evento_llegada()
    for p in lista_procesos_entrantes:
      print(f"\n>>> Llegada del proceso P{p.id} (tamaño: {p.tamano}, tiempo irrupción: {p.tiempo_irrupcion})")
      if self.check_multiprogramacion():
        print(f"    Multiprogramación alcanzada. Proceso P{p.id} agregado a cola de nuevos.")
        self.cola_procesos_nuevos.encolar(p)
        self.memoria.mostrar_estados(tipo_evento=f"llegada proceso P{p.id} - multiprogramación alcanzada")
      else:
        particion = self.memoria.buscar_particion_best_fit(p)
        if particion:
          particion.asignar_proceso(p)
          self.actualizar_cola_listo(p)
          self.planificar_proceso(p)
          self.memoria.mostrar_estados(tipo_evento=f"llegada proceso P{p.id} - asignado a partición {particion.id}")
        else:
          print(f"    No hay partición disponible. Proceso P{p.id} suspendido.")
          self.cola_listo_suspendido.encolar(p)
          self.memoria.mostrar_estados(tipo_evento=f"llegada proceso P{p.id} - suspendido (sin espacio)")
            
  def seleccionar_siguiente_proceso(self):
    """Selecciona el siguiente proceso de la cola de listo cuando la CPU está libre"""
    if self.cpu.esta_libre() and not self.cola_listo.esta_vacio():
      # Seleccionar el proceso con menor tiempo restante (SJF)
      siguiente_proceso = self.cola_listo.obtener_primero_por_tiempo()
      # Eliminar el proceso de la cola antes de asignarlo a CPU
      self.cola_listo.eliminar_proceso(siguiente_proceso)
      self.cpu.ejecutar_proceso(siguiente_proceso)
      if siguiente_proceso.tiempo_inicio_ejecucion is None:
        siguiente_proceso.registrar_inicio_ejecucion(self.reloj_global)

  def procesar_finalizaciones(self):
    proceso_actual = self.cpu.proceso
    if proceso_actual and proceso_actual.tiempo_restante == 0:
      # Registrar tiempo de finalización
      proceso_actual.registrar_finalizacion(self.reloj_global)
      print(f"\n>>> Finalización del proceso P{proceso_actual.id}")
      self.cola_terminado.encolar(proceso_actual)
      self.cola_listo.eliminar_proceso(proceso_actual)
      self.cpu.liberar_proceso()
      particion = self.memoria.get_particion_by_proceso(proceso_actual)
      if particion:
        particion.liberar_proceso()
        print(f"    Partición {particion.id} liberada")
      self.reubicar_procesos_suspendidos()
      self.memoria.mostrar_estados(tipo_evento=f"finalización proceso P{proceso_actual.id}")
      # Seleccionar siguiente proceso después de liberar la CPU
      self.seleccionar_siguiente_proceso()

  def avanzar_tiempo(self):
    if not self.cpu.esta_libre():
      self.cpu.proceso.tiempo_restante -= 1
    self.reloj_global += 1
    print("tiempo global:", self.reloj_global)

  def ejecutar(self):
    self.procesos_nuevos = self.lector_procesos.leer_procesos()
    self.length_procesos_nuevos = len(self.procesos_nuevos)

    if self.length_procesos_nuevos > 10:
      raise ValueError('Error, solo se permiten hasta 10 procesos en el archivo de entrada')

    if self.length_procesos_nuevos == 0:
      print("No hay procesos para ejecutar.")
      return

    # Agregar todos los procesos a la cola de nuevos
    for proceso in self.procesos_nuevos:
      self.cola_procesos_nuevos.encolar(proceso)

    # Condición de salida: cuando todos los procesos han terminado
    # O cuando no hay más trabajo que hacer (todos en terminado o no hay procesos activos)
    max_iteraciones = 10000  # Límite de seguridad para evitar bucles infinitos
    iteracion = 0
    
    while len(self.cola_terminado.procesos) < self.length_procesos_nuevos:
      iteracion += 1
      if iteracion > max_iteraciones:
        print(f"ADVERTENCIA: Se alcanzó el límite de iteraciones ({max_iteraciones}). Deteniendo simulación.")
        break
      
      # Verificar si hay trabajo pendiente
      procesos_pendientes = (
        len(self.cola_procesos_nuevos.procesos) +
        len(self.cola_listo.procesos) +
        len(self.cola_listo_suspendido.procesos) +
        (1 if not self.cpu.esta_libre() else 0)
      )
      
      if procesos_pendientes == 0 and len(self.cola_terminado.procesos) < self.length_procesos_nuevos:
        # No hay más trabajo pero no todos los procesos terminaron
        # Esto puede pasar si hay procesos que nunca llegaron
        print(f"ADVERTENCIA: No hay más trabajo pendiente pero solo {len(self.cola_terminado.procesos)}/{self.length_procesos_nuevos} procesos terminaron.")
        break
      
      self.procesar_llegadas()
      # Seleccionar siguiente proceso si la CPU está libre (antes de procesar finalizaciones)
      self.seleccionar_siguiente_proceso()
      self.procesar_finalizaciones()
      self.avanzar_tiempo()
    
    # Generar informe al finalizar
    self.generar_informes()
      