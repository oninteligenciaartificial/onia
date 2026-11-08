# Entrega instrumental y ensayo audiovisual separado

Corte 6/11/2026. Ingesta instrumental implementada y runtime CPU compilado; el primer control audiovisual no se ejecutó porque la adquisición de pesos quedó incompleta. No se analizó un reel con este modelo. El estado y el próximo paso se mantienen en [capacidad-audiovisual-001](../../continuidad/tareas/capacidad-audiovisual-001.json); el objetivo de analizar referentes continúa pendiente.

## Componente implementado

[audiovisual.py](../../scripts/audiovisual.py) recibe un medio local autorizado, verifica sus bytes antes/después de ffprobe y emite un recibo instrumental saneado. Sólo conserva identidad pública declarada, hash, tamaño y campos permitidos de pistas/contenedor. No descarga ni copia originales; no importa tags, rutas, cookies o stderr. Todas las capacidades perceptuales permanecen pendientes.

Ejemplo, desde la raíz del repo, usando dos directorios existentes:

```sh
python _investigacion-onia/base-operativa/scripts/audiovisual.py \
  --raiz-medios /ruta/autorizada --archivo reel.mp4 \
  --url https://www.instagram.com/reel/ID/ \
  --raiz-salida /ruta/recibos --salida ingesta-nueva.json
```

La identidad URL es declaración del operador; no prueba por sí sola procedencia de red. Límite de entrada 256 MiB; formatos mp4/mov/webm, demuxer fijo y protocolo file. Timeout de 20 s sólo para ffprobe. La salida usa temporal propio y publicación atómica por hardlink sin reemplazo; un filesystem incompatible produce fallo explícito, sin sobrescritura alternativa.

## Evidencia de esta unidad

- [Validación](../../continuidad/evidencias/capacidad-audiovisual-001/validacion-ingesta-v1.json): 23 tests, Windows 22 aprobados y una omisión por privilegio symlink; WSL local 23/23. Incluye clips sintéticos color+tono y video mudo con FFmpeg/ffprobe reales. No se repitieron suites anteriores sin cambios.
- Se corrigieron dos fallos concretos: estructura JSON anidada inválida provocaba excepción no saneada; una escritura interrumpida dejaba salida parcial. Las regresiones comprueban rechazo, no divulgación de rutas y conservación de archivos ajenos/concurrentes.
- [Original Cormac](../../continuidad/evidencias/capacidad-audiovisual-001/ingesta-cormac-v1.json): 10 749 782 bytes, SHA-256 9be4267480093249e104ec9821271e1a755e4329b7ea4d8fca3fc8bacd3b664e, duración de contenedor 37.753991 s, pistas VP9 y AAC. Metadata y hash coinciden; no se extrajeron conclusiones de guion, sonido, tipografía o edición.
- [Fuentes recibidas](../../continuidad/evidencias/capacidad-audiovisual-001/fuentes-corte-v1.json) y [preflight Cloud](../../continuidad/evidencias/capacidad-audiovisual-001/preflight-cloud-v1.json) distinguen cortes, entorno, comando y límites. El nuevo margen Cloud permite preparar un ensayo; no demuestra encaje ni valida producción VPS.

## Reglas, contexto, iniciativa y modelos

El runtime CPU/no-TTS se preparó en un workspace Cloud aislado. La copia local de `piloto-cloud/preparacion-v2` conserva 16 archivos con bytes y SHA-256 exactos; cinco regresiones pertinentes comprobaron SIGTERM, cierre incompleto, restauración y límites del supervisor. El primer build se cortó por wall a los 540,14 s y 96 %, sin procesos activos pendientes. Una continuación incremental explícita terminó con salida 0 en 69,55 s, conservando fuentes y objetos; siete archivos y su manifiesto se recuperaron exactos en `piloto-cloud/build-continuacion-v1`. [Recibo de compilación](../../continuidad/evidencias/capacidad-audiovisual-001/build-cloud-v1.json).

La [revisión de código congelada](piloto-cloud/revision-codigo-v2.md) permite la primera carga controlada, no acredita percepción. `piloto-cloud/ensayo-config-v1.json` fija un único negativo de dos segundos, contexto 2048, respuesta 128, señal gris y PCM cero, sin VAD ni TTS. El control y la consigna quedaron preparados, pero hubo **cero invocaciones del modelo**.

La transferencia terminó con `TimeoutError` y salida 1 a los 590,2766 s, junto al deadline interno de 590 s; el supervisor tenía wall de 600 s y no mató el proceso. LLM y audio quedaron completos, con tamaño y SHA-256 verificados mediante lectura del archivo cerrado. Visión conserva 171 966 464 bytes parciales, que no se aceptaron como peso. El texto exacto de la excepción se omitió al sanear URLs firmadas: no se puede precisar su punto de origen ni atribuir un fallo HTTP. No hubo procesos propios activos pendientes, reintentos o positivos. [Recibo del intento](../../continuidad/evidencias/capacidad-audiovisual-001/cierre-intento-v1.json).

## Almacenamiento del corte

Bytes aparentes medidos en el workspace Cloud, sin duplicar destinos de symlinks. [Inventario completo y RAM separada](../../continuidad/evidencias/capacidad-audiovisual-001/almacenamiento-v1.json).

| Artefactos en Cloud | Bytes |
|---|---:|
| Pesos LLM y audio completos y verificados | 5 686 882 304 |
| Peso de visión parcial, no validado | 171 966 464 |
| Runtime/código y build/CMake | 386 330 593 |
| Cuatro archivos de controles | 65 664 |
| Logs, recibos y ZIP | 5 227 092 |
| Total, incluyendo metadatos de directorios y symlinks | 6 253 986 668 |

El filesystem reportó 6 281 113 600 bytes en bloques y 57 849 610 240 bytes libres. Son medidas de disco; el límite visible de RAM de 32 GiB es otro recurso. La descarga alcanzó 19 472 384 bytes de RSS muestreado; **RAM y consumo del modelo no se midieron**, porque no se cargó.

En el PC quedaron 65 archivos textuales del piloto (356 293 bytes), además de scripts, pruebas, informes y recibos locales; no se copiaron pesos al PC. El reel original de 10 749 782 bytes ya existía y la ingesta no lo duplicó. El VPS sólo recibió consultas de lectura: sin modelos instalados, medios copiados ni despliegue de esta unidad.

Se observó persistencia de los artefactos Cloud entre turnos concretos; no se contrató ni decidió almacenamiento permanente. Los parciales se conservan. Por instrucción de Sergio se cierra este intento y se espera la selección del stack antes de nuevas tentativas. Una futura retoma debe cotejar marcadores, manifiestos y bytes conservados; el primer negativo sigue pendiente y no debe contarse como fallo semántico del modelo.

## Lecciones comprobadas y siguiente paso

- Preparar y compilar no equivale a ver u oír un reel. Esta unidad tiene 23 pruebas de ingesta y build correcto, pero cero inferencias AV; el reconocimiento y la RAM del modelo siguen sin evaluar.
- Leer el header o la documentación no basta para acreditar consumo de señal: la implementación ignoraba texto y retornos, omitía medios y podía contar audio reservado como leído. Las correcciones y sus fuentes quedaron fijadas; no se reescribieron los informes históricos para esconderlas.
- La revisión separada encontró fallos de SIGTERM, descendientes vivos y dimensión del projector. Los controles de supervisor y el único escritor permitieron corregirlos antes de cargar pesos. Una aprobación de código sigue siendo distinta de un resultado perceptual.
- Los tiempos deben corresponder a la fase: build detenido a 540,14 s, continuación incremental de 69,55 s y transferencia fallida de 590,28 s. No son tiempos de análisis de video ni consumo CPU medido. Un presupuesto conservador puede cortar preparación; se conserva el recibo antes de decidir una continuación, sin reiniciar lo ya compilado.
- La compacción produjo una retoma del objetivo antiguo en la revisora. Registro canónico, rol y próxima entrega recuperaron el encargo mediante una intervención explícita; no se demostró continuidad automática. El incidente permanece enlazado abajo.
- La descarga acotada preservó dos pesos verificables y un parcial sin cargar un modelo incompleto. El saneado del error perdió la distinción entre deadline propio y otro timeout; una futura implementación debe conservar un código de causa seguro, sin URLs firmadas, antes de volver a medir.
- Reutilizar chats no cambió su modelo. La regla ya existente en `ORQUESTACION.md:33` exigía cotejar recomendado, solicitado y observado; faltó aplicarla antes del despacho. El último `turn_context` propio del turno activo acredita Astra/ultra, aunque este cierre se solicitó con Sol medio. Se conserva esa discrepancia y los antecedentes, sin afirmar un cambio efectivo ni ahorro porcentual. Para cierres simples se recomienda Sol medio; para implementación/revisión compleja, Sol alto; escalar sólo por una causa documentada. [Evidencia de modelos y cuota informada por coordinación](../../continuidad/evidencias/capacidad-audiovisual-001/modelos-cierre-v1.json).

La [revisión final del intento](../../continuidad/evidencias/capacidad-audiovisual-001/revision-cierre-v1.json) confirma estos límites: el gate del driver sólo fue revisado estáticamente y 2048/128 son parámetros solicitados, no observados en una inferencia.

La aplicación comprobada de este cierre consiste en guardar evidencia, lecciones y ficha de ejecución distinguiendo solicitud y observación, conservar los cortes anteriores y liberar la asignación. No representa entrenamiento de modelos, operación automática 24/7 ni compacción perfecta. Se termina el turno sin nuevas pruebas o esperas; coordinación comprobará un único turno corto posterior con Sol medio. La cuota es compartida: el corte informado de 92 % consumido y 8 % restante no se reparte por chat ni se presenta como consumo de este ensayo.

Actualización posterior de coordinación: el turno corto `01a1b344-dd0d-7502-846c-3139bb9f93e2` terminó sin herramientas ni tareas activas. Su `turn_context` de 2026-11-06T23:49:57.233Z acredita **gpt-6.1-sol / medium**; el cambio efectivo se verificó al iniciar un turno nuevo. [Recibo de coordinación](../../continuidad/evidencias/capacidad-audiovisual-001/coordinacion-cambio-modelo-v1.json). Esto conserva el antecedente Astra/ultra del turno anterior y no acredita cambios en otros chats ni un porcentaje de ahorro.

**Restricción vigente de Sergio: componentes open source.** Las [opciones investigadas](opciones-open-source.md) proponen cerrar primero una combinación CPU de FFmpeg, fuente OFL y faster-whisper small con Silero VAD para transcripción. Ese ASR tiene evidencia previa acotada, no ejecución nueva en esta unidad, y no acredita música, prosodia o comprensión AV. HyperFrames se mantiene como opción de producción con dependencias por resolver para una pila estrictamente abierta; no es un transcriptor. MiniCPM queda experimental. Codex/Cloud no se presentan como software abierto. La selección final, cuota y posibles cambios de modelo pertenecen a la coordinación; aquí no se instalaron esas propuestas ni se bajó ningún modelo conversacional.

| Criterio | Comprobado en esta unidad | Límite |
|---|---|---|
| Reglas | Fuentes canónicas, escritores delimitados, informes de corte preservados y pruebas de errores/integridad. | Una comprobación no garantiza obediencia universal. |
| Contexto | Registro único y retoma dirigida después de un evento real de compacción de la revisora. | El primer comentario posterior retomó un objetivo anterior de onia/iPhone; no está resuelta la continuidad automática. [Incidente y respuesta posterior](../../continuidad/evidencias/capacidad-audiovisual-001/incidente-contexto-v1.json). |
| Iniciativa | Ingesta local ejecutada; se buscó un entorno Cloud ya disponible frente al margen VPS insuficientemente demostrado. | No se amplían gasto, servicios, permisos o publicación. |
| Modelo por capacidad | Recomendación de coordinación/código separada de candidato AV; recomendado/solicitado/observado no se rellenan por inferencia. | Modelo conversacional no equivale a receptor audio/video; MiniCPM-o4.5 aún requiere controles de su configuración. |

El [protocolo](PROTOCOLO.md) conserva presupuesto, controles, conteos por modalidad, contexto sin recortes, revisión independiente y condiciones para el piloto. Guion, edición, voz, música, SFX, tipografías y afirmaciones se aceptarán por atributos respaldados, sin convertir una unidad instrumental en comprensión del video.
