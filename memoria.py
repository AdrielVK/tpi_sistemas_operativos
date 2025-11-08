from particion import Particion
from proceso import Proceso

class Memoria:
  particiones: list[Particion]


  def __init__(self):
    particion_SO = Particion(1, 100, 1, 0)
    particion_1 = Particion(2,250,101,0)
    particion_2 = Particion(3,150,352,0)
    particion_3 = Particion(4,50,504,0)

    self.particiones = [particion_SO, particion_1, particion_2, particion_3]
    

  def buscar_particion_best_fit(self, proceso:Proceso)-> Particion | None:
    tamanio_proceso = proceso.tamano
    particion_adecuada:Particion | None = None
    diferencia:int| None = None

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

