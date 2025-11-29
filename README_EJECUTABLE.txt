INSTRUCCIONES PARA USAR EL EJECUTABLE
=====================================


CÓMO USAR:
----------
1. Ejecuta el archivo SimuladorProcesos.exe haciendo doble clic sobre él
2. El programa te pedirá que ingreses el nombre del archivo CSV (sin la extensión .csv)
   Por ejemplo, si tu archivo se llama "procesos2.csv", solo ingresa: procesos2
3. El programa procesará la simulación y mostrará los resultados en la terminal del sistema operativo en el que se este ejecutando
4. Luego de visualizar los resultados, se debe presionar Enter para cerrar el ejecutable.


CONSIDERACIONES:
---------------
1. La ubicacion de los archivos .csv deben estar colocador a la misma altura del ejecutable, o a la misma altura y dentro de una carpeta "inputs". Con esto, respetando lo anterior, se puede ejecutar en cualquier directorio el programa.

2. FORMATO DEL ARCHIVO CSV:
------------------------
El archivo CSV debe tener el siguiente formato:
id,llegada,tamano,irrupcion

Ejemplo:
e1,0,52,18
e2,1,58,4
e3,2,59,20

Los tipos de datos deben ser los siguientes:
id: string
llegada: entero
tamano: entero
irrupcion:entero

NOTAS:
------
- El ejecutable incluye todos los módulos necesarios, no necesitas instalar Python
- El ejecutable es independiente y puede ejecutarse en cualquier computadora Windows
- Si tienes problemas, asegúrate de que el archivo CSV tenga el formato correcto

