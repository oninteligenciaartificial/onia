# Caso desarrollo · fixture sintética v1

No contiene datos privados ni acceso real. No es salida de un brazo.

## Tarea
Corregí sólo select_latest(events) de fixture.py en una solución independiente solution.py. Entregá el archivo y explicación de causa/prueba. Contrato: lista de dicts con id y seq entero no negativo; devolver último evento con seq máximo, empate se resuelve por última aparición; [] devuelve None; no mutar entrada. No ampliar validación de datos ni usar paquetes externos.

## Fuentes provistas
Fixture sintética de selector de eventos; sin repo de producto. El fallo reportado: para seq 9 y 10 retorna 9. La función actual ordena lexicográficamente y muta la lista. El objetivo incluye desempate y no mutación definidos en contrato.

