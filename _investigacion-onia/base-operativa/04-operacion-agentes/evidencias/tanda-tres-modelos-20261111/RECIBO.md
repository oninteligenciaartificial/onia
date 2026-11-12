# Tanda real de tres sesiones · 11 de noviembre de 2026

El lanzador directo del harness abrió dos ejecutoras con rutas independientes y una revisora. Entre las 22:10:59 y las 22:13:37 de La Paz, 19 lecturas consecutivas del registro encontraron los tres procesos vivos, con los mismos hilos. Cada perfil observado se obtuvo de un contexto de turno y su evento de uso del mismo hilo y turno. El tercer cupo quedó reservado a la revisión de la entrega de custodia ya publicada.

| Encargo | Rol | Hilo de Codex | Perfil solicitado | Perfil observado | Hijos permitidos |
| --- | --- | --- | --- | --- | --- |
| `despachador-hijos-20261111` | Ejecutora | `01a1cd85-8cde-7730-9da2-a0d8cc523a30` | `gpt-6.1-sol high` | `gpt-6.1-sol high` | 1 |
| `recibo-modelos-harness-20261111` | Ejecutora | `01a1cd85-c575-7ab3-96ae-afa6af9bb941` | `gpt-6.1-sol low` | `gpt-6.1-sol low` | 0 |
| `ensayo-cuatro-control-20261112` | Revisora | `01a1cd85-a10c-7df2-adb6-822a008364fc` | `gpt-6.1-sol high` | `gpt-6.1-sol high` | 0 |

La primera ejecutora delegó una lectura acotada de las rutas de lanzamiento y retoma al hilo `01a1cd85-ef51-7663-9c64-30bfc05c5c62`. Perfil solicitado y observado `gpt-6-luna high`. El padre publicó el cambio. Los cupos quedaron libres conforme terminaron sus procesos y se recogieron los resultados o se preparó la siguiente revisión.

La revisora de la tanda dio **cambios** sobre `876778e2c9f0ca0c9f5dfc8425c6aa38f16a1f87`. Pasaron 41 comprobaciones en memoria y la prueba de compuertas. Pidió adjuntar las salidas vigentes de pruebas y del ensayo porque su sandbox de lectura impedía reproducir la suite con temporales. El [dictamen de ese cupo](../ensayo-cuatro-control-20261112/revision-9-273c6c41.json) conserva el motivo. La comprobación de cuatro simultáneas sigue pendiente. Los dos ensayos acotados se detuvieron con dos y tres procesos principales, respectivamente, por contención del registro y saturación. Ambos terminaron con cero procesos propios, reservas y custodias. El límite operativo sigue en tres.

## Productos y comprobación

- Despachador en `03b23daec252f638b704508d62731775f2438e29`. Aceptado sobre esa revisión, con 43 pruebas. El manifiesto admite 0, 1 o 2 hijos por ejecutora, con cero al omitir el campo y cero para la revisora. El mismo valor se aplica al lanzar, retomar y reconocer una sesión. La prueba de reinicio recupera el mismo hilo de una ejecutora con un hijo. [Pruebas](../despachador-hijos-20261111/PRUEBAS-coordinadora.txt) · [Dictamen](../despachador-hijos-20261111/revision-2-852a6533.json)
- Lector en `74c01ceeab5f3707155af158a98e678ce6bdf4c3`. Aceptado sobre esa revisión, con 18 pruebas. El lector rechazó la carpeta completa de sesiones y confirmó los cuatro perfiles al recibir únicamente los cuatro registros exactos. Se conservaron sólo los campos saneados. [Pruebas](../recibo-modelos-harness-20261111/PRUEBAS-coordinadora.txt) · [Dictamen](../recibo-modelos-harness-20261111/revision-3-1abe3133.json)
- Integración de ambos productos en `c46d0c0403ef5eaa7596d0b3c590177a7a2b5309`. Desde `05-herramientas/scripts`, `python3 -B -m unittest -q test_harness_lote test_perfiles_observados` devolvió `Ran 61 tests` y `OK`. El despachador instalado en el VPS se cotejó byte a byte con el integrado.

## Primera pasada del workshop

`harness_lote.py tick --cuota-codex` lanzó `workshop-arranque-venta-20261111`. El registro confirmó una ejecutora `01a1cd90-b189-7ff2-ab65-4ff56423382d`, Sol Low y cero hijos. La segunda pasada devolvió `sin_avance` con cero eventos y el registro conservó la misma sesión. Se dejó correr la preparación del paquete de grabación, VSL e inscripción. La operación comercial requiere el ensayo controlado y la decisión de Sergio. [Encargo](../../encargos/workshop-arranque-venta-20261111.md) · [Cierre de venta](../../../05-herramientas/fabrica-onia/CIERRE-VENTA-20261111.md)
