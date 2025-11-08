from particion import Particion
from proceso import Proceso
from typing import Optional, List

class Memoria:
  particiones: List[Particion]


  def __init__(self):
    particion_SO = Particion(1, 100, 1, 0)
    particion_1 = Particion(2,250,101,0)
    particion_2 = Particion(3,150,352,0)
    particion_3 = Particion(4,50,504,0)

    self.particiones = [particion_SO, particion_1, particion_2, particion_3]
  
  def get_particion_by_proceso(self, proceso: Proceso):
    for particion in self.particiones:
      if particion.proceso and particion.proceso.id == proceso.id:
        return particion

  def mostrar_estados(self, tipo_evento:str):
    print(f"\n{'='*70}")
    print(f"ESTADO DE MEMORIA - Evento: {tipo_evento}")
    print(f"{'='*70}")
    print(f"{'Particion':<12} {'Direcciones':<15} {'Tamaño':<10} {'Estado':<12} {'Fragmentación':<15}")
    print(f"{'-'*70}")
    
    for p in self.particiones:
      estado_proceso = f"P{p.proceso.id}" if p.proceso else "LIBRE"
      direccion_fin = p.direccion_inicio + p.tamano - 1
      direcciones = f"[{p.direccion_inicio:3d}-{direccion_fin:3d}]"
      print(f"{'Partición ' + str(p.id):<12} {direcciones:<15} {p.tamano:<10} {estado_proceso:<12} {p.fragmentacion_interna:<15}")
    
    print(f"{'='*70}\n")

  def buscar_particion_best_fit(self, proceso:Proceso)-> Optional[Particion]:
    tamanio_proceso = proceso.tamano
    particion_adecuada: Optional[Particion] = None
    diferencia: Optional[int] = None

    for particion in self.particiones:
      if particion.esta_libre() and particion.id != 1:
        if diferencia is None:
          particion_adecuada = particion
          diferencia = (particion.tamano - tamanio_proceso)
        elif (particion.tamano - tamanio_proceso) < diferencia:
          particion_adecuada = particion
          diferencia = (particion.tamano - tamanio_proceso)
    return particion_adecuada
    

  def check_espacio_disponible(self):
    for particion in self.particiones:
      if particion.esta_libre() and particion.id != 1:
        return True
    return False

  def registro_valla_so(self, direccion) -> bool:
    if direccion <= 101: 
      return False
    return True

  def liberar_particion(self, particion: Particion):
    pass

