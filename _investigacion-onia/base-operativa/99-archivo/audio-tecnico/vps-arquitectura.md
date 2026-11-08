# Diseño propuesto: análisis audiovisual en VPS

Estado: diseño, 5/11/2026. Responsable de ejecución futura: Desarrollo; aceptación de referentes: Jefa. El acceso SSH y un inventario puntual de recursos y servicios fueron comprobados: [informe vigente](vps-repositorio-20261105.md). Los componentes y nombres de este diseño siguen siendo propuestas; no se instaló el servicio. La prioridad inmediata sigue siendo terminar referentes con evidencia; este diseño no completa ese objetivo.

## Componentes y límites

- **Ingesta y medios:** reutilizar el corpus autorizado y sus manifiestos, hashes, duración y procedencia existentes en `audio-tecnico/README.md` y el almacenamiento de operación allí referenciado. Registrar origen, versión y derivados; mantener originales inmutables y no duplicar datos privados en Git. Retención, cifrado y capacidad efectiva se deciden tras inventario; borrar temporales sólo conforme a una política aprobada.
- **ASR:** transcribir voz con marcas temporales y confianza cuando el motor las proporcione. No certifica sonidos, emoción ni mezcla; guardar salida y versión sin presentar texto automático como revisión humana.
- **Eventos sonoros:** detectar candidatos de voz, música, efectos y silencios con controles conocidos. No equiparar clasificación a escucha fiable, prosodia o mezcla. Conservar respuestas y errores por modelo y configuración.
- **Video y sincronía:** extraer fotogramas o clips con mapa de tiempos y analizar orden/movimiento según cobertura explícita. Sincronía exige evidencia temporal conjunta de audio y video; ni fotogramas aislados ni ASR la acreditan.
- **Coordinador batch y workers:** cola persistente con estados pendiente, en ejecución, terminado y fallido; identificador, procedencia, intentos limitados, versiones, recursos y error. Trabajos reanudables e idempotentes, cancelables por unidad. No abrir endpoints públicos para las pruebas; acceso privado y mínimo necesario.

Repositorios, commits, modelos, pesos, licencias de código y pesos, dependencias y tamaños quedan **por seleccionar y fijar** después de medir CPU, RAM disponible, disco, GPU, carga y reservas. Gratis no implica que quepan ni que sean fiables. No repetir Eureka, MiDasheng o configuraciones ya rechazadas sin identificar y comprobar una causa corregida. Versiones y hashes acompañarán cada resultado; mantener fallos, incluido silencio, como evidencia.

## Datos e aislamiento

Nombres siguientes son ilustrativos, no infraestructura existente. La separación mínima exigida es **bases de datos distintas**, no esquemas distintos en una misma base:

| Dominio / dueño funcional | Base propuesta | Acceso, red y almacenamiento |
|---|---|---|
| Plataforma / responsable de producto | `plataforma_db` | Usuario y credenciales propios; sólo servicios de plataforma. Conservar instancia existente y su configuración hasta inventario. Volúmenes y respaldos propios. |
| Análisis / Desarrollo | `analisis_av_db` | Usuario limitado a su base; estado de jobs, manifiestos y referencias a medios, no medios binarios por defecto. Worker y coordinador en red interna privada. Volumen y respaldo propios; medios en almacenamiento separado con control de acceso. |
| Automatizaciones y otros usos / responsable de cada servicio | `automatizacion_db` y base distinta por uso cuando corresponda | Usuarios, credenciales, volúmenes y respaldos independientes; sin permisos cruzados por conveniencia. Intercambio por interfaz autorizada y acotada, no acceso directo a la base de plataforma. |

Evaluar una **instancia PostgreSQL independiente para análisis** para no alterar Supabase/Postgres existente: elegirla sólo después de medir recursos y configuración; si no cabe, no asumir que compartir instancia sea seguro. Aun compartiendo instancia, mantener bases, roles, secretos y respaldos separados. Sin puertos de base públicos, privilegios administrativos compartidos ni secretos en Git. Credenciales en mecanismo protegido existente o uno aprobado tras inventario; no copiar credenciales entre servicios. Ninguna migración de producción por defecto: una propuesta específica debe incluir respaldo, prueba de restauración, ventana, verificación y reversión antes de tocarla.

Cada servicio mantiene backup independiente de su base y configuración recuperable; análisis respalda también manifiestos y medios necesarios según política de retención. Cifrar y proteger copias, registrar versión, fecha y destino, y ensayar restauración aislada con comprobación de integridad; un backup no probado no acredita recuperación. No inventar frecuencia ni almacenamiento disponible antes de medir.

## Ejecución posterior al acceso

1. Confirmar host y acceso; inventariar sólo lectura CPU, memoria libre, disco, GPU, carga y servicios/volúmenes/redes activos sin revelar secretos. Establecer reservas y límites explícitos de CPU, RAM, disco, concurrencia y tiempo según medición; si no hay margen, detener la instalación y comunicar la necesidad concreta sin compras ni ampliar plan.
2. Elegir una única ruta compatible, revisar fuentes oficiales, licencia, dependencias y arranque; fijar commit y hashes. Preparar directorio y entorno propios, sin upgrades del sistema, puertos públicos ni cambios en apps existentes. Instalar únicamente tras comprobar margen y aislamiento. Registrar cambios y rutas para reversión.
3. Ejecutar primero silencio sintético con instrucción neutral y sin VAD que lo oculte; conservar la salida incluso si falla. Si pasa, ejecutar controles positivos conocidos y controles de orden/temporalidad antes de aplicar al corpus. Separar pruebas de transcripción, eventos y percepción/mezcla/sincronía; no atribuir una capacidad que el control no mide. Si falla, detener esa ruta y registrar condiciones y resultado.
4. Sólo tras pasar controles relevantes, procesar muestras autorizadas conservando trazabilidad y límites de cobertura. Verificar efectos sobre cargas existentes. Para revertir, detener sólo los procesos propios, retirar sólo los recursos creados para el ensayo tras verificar rutas y dependencias, y preservar evidencia; no tocar datos o servicios ajenos. Si hay incertidumbre, detenerse antes de borrar.

**Aceptación:** inventario y reservas verificadas; bases y credenciales separadas comprobadas; recuperación ensayada; controles pertinentes y resultados reproducibles registrados, sin degradar servicios existentes. Un contenedor activo o una transcripción aislada no demuestran comprensión acústica integral ni cierran referentes.

## Hechos de continuidad

La ausencia de IAB no demostraba ausencia de Computer Use Windows: se inicializó `@oai/sky` y se abrió Chrome, pero su guard detuvo la lectura por no poder determinar la URL. Hay archivos de identidad SSH locales, sin vinculación ni acceso al VPS acreditados. Modelos ejecutados anteriormente produjeron resultados, pero los controles fallidos impiden tratarlos como fiables para el objetivo. Posteriormente se comprobó el acceso SSH y se midieron recursos y servicios en una captura puntual; el detalle y el límite de verificación de huella están en el [inventario vigente](vps-repositorio-20261105.md). No se instaló software allí. Faster-whisper y YAMNet son propuestas parciales, no solución aceptada de la brecha integral.

## Diseño ejecutable propuesto para referentes · 5/11/2026

**Sin instalación en esta tanda.** Inventario puntual y límites en [vps-repositorio](vps-repositorio-20261105.md). Un worker batch privado y secuencial con máximo inicial 2 CPU, 3 GiB y 10 GiB de trabajo; detener ante disponible menor de 6 GiB, disco menor de 30 GiB o degradación. Revalidar condiciones antes de empezar. Estos límites son hipótesis operativas, no garantías ni benchmark.

### Módulos parciales

1. ASR: [faster-whisper v1.2.1](https://github.com/SYSTRAN/faster-whisper/releases/tag/v1.2.1), código [MIT](https://github.com/SYSTRAN/faster-whisper/blob/master/LICENSE), CPU int8. Reutilizar el checkpoint y controles previamente registrados en [README](README.md), fijar hash, licencia y dependencias exactas antes de transferir; no suponer que la velocidad local se repetirá. Salida con texto, tiempos, versión y errores; contraste humano de nombres, cifras y términos dudosos.
2. Eventos: [YAMNet oficial](https://github.com/tensorflow/models/tree/master/research/audioset/yamnet), código Apache 2.0; fijar commit, hash/licencia de pesos y dependencias antes de instalación. Su documentación exige Keras 2, incompatible con Keras 3. Produce candidatos de 521 clases, no escucha validada ni interpretación de mezcla. El umbral de decisión debe calibrarse con controles y registrar puntuaciones crudas, no tratar la clase máxima como certeza.
3. Video: extracción de fotogramas y segmentos con tiempo de origen; registrar cobertura e intervalos omitidos. Revisar imagen, textos, montaje y secuencia con evidencia visual; muestreo no prueba movimiento continuo. Comparar tiempos de voz, eventos y cortes para proponer sincronías, sujetas a control temporal y revisión.

El servicio persistente futuro usa base de análisis separada de plataforma y automatizaciones, rol/credenciales y volumen/respaldo propios, red privada sin puertos públicos; se decidirá instancia propia al medir margen. Probar restauración aislada. Para el primer ensayo sintético bastan archivos de resultados, sin crear base ni tocar PostgreSQL existente. Guardar medios autorizados fuera de Git, manifiesto con origen/hash y salidas separadas por versión.

### MiniCPM-o 2.6: candidata no habilitada

La [ficha oficial del modelo](https://huggingface.co/openbmb/MiniCPM-o-2_6) declara Apache 2.0 para código y pesos y una encuesta opcional. Aunque presenta capacidades generales de audio y video, su apartado específico de llama.cpp limita MiniCPM-o 2.6 a **visión solamente**. La misma ficha indica 7 GB de memoria GPU para int4, cifra de VRAM que no es medición de RAM CPU ni acredita procesadores de audio/video. No se identificó una revisión concreta, pesos y runtime oficiales que prueben audio y video en CPU ni su RAM pico. Por tanto no hay instalación ni descarga habilitada para esta candidata; no se concluye imposibilidad universal. Los 10 GiB disponibles observados son una captura, y reservando 6 GiB quedarían aproximadamente 4 GiB antes de otros cambios de carga: no se puede comparar una necesidad CPU desconocida con ese margen ni ampliar el límite de 3 GiB por suposición.
### Controles de aceptación

Silencio digital primero, entrada completa sin VAD que lo oculte, instrucción neutral fija: cero eventos inventados; preservar respuesta. Si falla, detener esa ruta. ASR: silencio y tono sin texto, frase sintética conocida sin omitir palabras esenciales ni inventar contenido; conservar transcripción literal. Eventos: controles positivos de voz, música y efecto aislado y negativos cruzados; detectar cada evento conocido sin afirmar uno ausente. Orden visual: identificar correctamente orden de dos acciones sintéticas y no invertirlo. Temporalidad/sincronía: señales y cortes sintéticos con tiempos conocidos; aceptar sólo si localización y relación antes/después coinciden dentro de ±0,5 s, sin eventos espurios. Prosodia/mezcla: conjunto de ejemplos con juicio humano y rúbrica previa; sin ese contraste no hay aceptación. Son criterios mínimos para este piloto, no tasas de precisión general ni validación automática de referentes.

Tiempo, RAM pico y carga se miden, no se prometen. Si el candidato no cabe o falla silencio, continuar el análisis verbal/visual con evidencia y usar revisión humana acotada de fragmentos y mapa temporal para sonidos, prosodia y sincronía; registrar qué sigue sin verificar y no cerrar el objetivo integral hasta completar esa revisión. Siguiente acción: tras aceptación del diseño, Desarrollo prepara los módulos parciales y ejecuta los controles permitidos con reservas; Jefa coordina la revisión perceptual humana acotada de los fragmentos aún no verificables e integra evidencia por referente en el cerebro de marca, sin atribuir certeza a etiquetas automáticas.
