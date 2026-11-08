# Cierre del piloto Cormac y método de vídeo

6 de noviembre de 2026, America/Caracas. **Ficha útil terminada con ASR y lectura visual por muestreo; ruta audiovisual conjunta no aceptada.** El negativo de silencio pasó y el positivo de voz/orden falló. No se ejecutó esa configuración sobre Cormac. La capacidad integral sigue pendiente.

Entrega principal: [Cormac Hayden, `cormachdn`, reel DfWLWspIruU](FICHA-CORMAC.md). Registro único: [capacidad-audiovisual-001](../../04-operacion-agentes/tareas/capacidad-audiovisual-001.json). Los cortes y recibos anteriores permanecen intactos.

## Resultado modular vigente

[Informe breve de edición/textos](lectura-modular-cormac.md): 2264/2264 frames con PTS; tres cortes de contenido confirmados y dos reencuadres; tres candidatos subumbral conservados como ambiguos. No detector exhaustivo ni cadencia exacta. Fin de vídeo37,733333s, distinto del contenedor37,753991s. Se reutilizó ASR.

Tesseract5.5 aislado produjo1/6 coincidencias literales contra referencia previa de un agente de visión; negativo con falso positivo. Se conservan texto visual revisado, errores crudos y límites. Scan15,59s, seisOCR1,76s; pico grupal muestreado242,54MB; sin nuevas inferenciasAV/audio, cambios globales o publicación. [Dictamen modular](../../04-operacion-agentes/evidencias/capacidad-audiovisual-001/revision-modular-cormac-v1.json). Los resultados AV anteriores siguen como historia, sin rehabilitarlos.

## Resultado del contenido y cobertura

La ficha identifica la cuenta publicadora y resume guion, composición, subtítulos, alternancia cara/escritorio/repositorio y afirmaciones del autor. Distingue mecanismos referenciados de promesas sin resultado final comprobado. Alex Carrera es otra pieza; no se inició otro análisis.

- ASR existente de la pista completa: 18 segmentos locales y 11 VPS, 154 unidades normalizadas por salida, similitud 0,993506; única sustitución Halo/Halos. Son candidatos automáticos, sin corrección humana; tiempos aproximados. No hubo nueva transcripción.
- Imagen: 38 muestras existentes, preparación documentada a 1 Hz, examinadas en las dos hojas. Sin PTS individual verificado en esta retoma, visionado continuo o medición fina de cortes. La tipografía exacta no está acreditada.
- AV conjunto de Cormac: **0 s**. No se presenta la propuesta de 3 s como análisis del reel completo. Tras fallar el positivo no se lanzaron ventanas del reel. Música, efectos, prosodia y sincronía fina permanecen sin evaluar.

Se eligió **FFmpeg + faster-whisper + Silero**. El ASR con VAD tiene evidencia previa acotada; no es un servicio activo ni valida sonido no verbal. [Opciones y dependencias](opciones-open-source.md): HyperFrames es una opción de producción con GSAP por resolver para apertura estricta, no un transcriptor. Codex/Cloud no se presentan como software abierto.

## Pruebas reales de esta ruta

| Etapa | Resultado |
|---|---|
| Ingesta instrumental | 23 pruebas definidas: WSL 23/23, Windows 22 y una omisión por privilegio symlink. No se repitieron en esta retoma. |
| Runtime CPU | Build inicial cortado a 540,14 s; continuación incremental exit0 en 69,55 s. Fuentes y bibliotecas fijadas, sin nueva compilación. |
| Primera adquisición | TimeoutError a 590,28 s; LLM/audio completos y visión parcial. Cero inferencias entonces. Punto exacto del timeout no conservado. |
| Continuación de visión | HTTP206/rango correcto; 923 146 720 bytes añadidos; SHA final válido. No se volvieron a descargar LLM/audio. 173,04 s. |
| Negativo gris/silencio, 2 s | Una inferencia, exit0 en 135,60 s. Dos pares aceptados, 338 posiciones frente a 2048; gris, silencio y ausencia de cambios. Aceptado sólo este control. |
| Driver positivo v1 | Guard del prompt antiguo rechazó antes de cargar modelo: 0 inferencias. Fallo conservado; corrección puntual de la ruta en v2. |
| Positivo de voz/figuras/orden, 2 s | Una inferencia real, exit0 en 133,61 s y modalidades aceptadas. No reconoce voz/one two, omite silencio final y no establece claramente la secuencia. Criterio semántico fallido. |

Verdad del positivo: flite kal16 ya incluido generó one two, 13 823 muestras completas, ceros hasta 1 s; figura roja a izquierda. Segundo segundo: 16 000 ceros y figura azul a derecha. No hubo audición humana ni se pasó la verdad al modelo. La respuesta habla de cambios de tono y simultaneidad; no permite llamar inventado a todo cambio de tono ni medir sincronía falsa.

La revisora cotejó tamaños, SHA, código de generación, driver, corrección de ruta, argv, salida literal, telemetría y limpieza. Negativo: 21/21 archivos; positivo v1: 17/17; positivo v2: 18/18; transferencia: 7/7. [Recibo del negativo](../../04-operacion-agentes/evidencias/capacidad-audiovisual-001/negativo-aceptado-v1.json), [cierre de Cormac](../../04-operacion-agentes/evidencias/capacidad-audiovisual-001/cierre-cormac-v1.json) y [dictamen final](../../04-operacion-agentes/evidencias/capacidad-audiovisual-001/revision-final-cormac-v1.json).

## Medio y consumo

El original local conserva 10 749 782 bytes y SHA 9be4267480093249e104ec9821271e1a755e4329b7ea4d8fca3fc8bacd3b664e. Las dos pistas de la misma pieza pública se recuperaron en Cloud sin cookies ni instalaciones. Streamhash de ambos payloads coincide con el original; el remux tiene 10 749 773 bytes, SHA 2c89164b66a9c556e749b789e0ca2004562c859316ac447ba883f7535f5a79a5 y duración declarada 37,78 s. No se acredita identidad binaria o equivalencia exacta de timestamps. [Recibo saneado](piloto-cloud/cormac-transfer-v1/transfer-receipt.json); URLs temporales fuera de la exportación.

| Almacenamiento Cloud | Bytes del corte |
|---|---:|
| Tres pesos completos | 6 781 995 488 |
| Runtime/código y build/CMake conservados | 386 330 593 |
| Pistas Cormac y remux | 21 492 997 |
| Controles, logs, recibos y metadatos restantes, por diferencia del muestreo | 9 930 771 |
| Árbol propio, último muestreo | 7 199 749 849 |

Disco libre reportado: 56 903 532 544 bytes. Son medidas de disco, distintas del límite visible de RAM de 32 GiB. Las dos inferencias de control sumaron 269,21 s de pared incluyendo sus fases; máximo RSS muestreado 10 784 448 512 bytes, no pico exacto ni garantía para VPS. CPU real no capturada. Hay timestamps de carga y tiempos del encoder visual; prefill/decode no quedan separados. [Recursos del cierre](piloto-cloud/positivo-v2/closing-resources.json).

El PC conserva original, ASR, hojas y copias textuales de código/recibos, sin pesos nuevos. El VPS no recibió instalaciones, medios o cambios de servicio en esta retoma; se reutilizó su ASR histórico. La persistencia Cloud se observó entre turnos concretos y no equivale a almacenamiento permanente contratado. No hubo publicación Git o despliegue.

## Lecciones aplicadas y próximo paso

- Preparación, build, recepción de embeddings y exit0 no prueban comprensión. El positivo impidió usar una configuración no validada para atribuir sonidos al reel.
- La implementación real ignoraba texto/retornos y podía contar audio reservado. Correcciones, pruebas de supervisor y cortes quedaron fijados; la documentación sola no acreditaba capacidad.
- Un driver apuntó al prompt antiguo. El guard detectó la discrepancia antes de inferir; se conservó el error y sólo se corrigió la referencia en un corte nuevo. No se cambió el criterio después de ver el resultado.
- El timeout de adquisición preservó dos pesos y el parcial. La retoma comprobó HTTP Range y SHA antes de usarlo. Conviene conservar un código seguro de causa del timeout, sin perderlo al sanear URLs.
- La compacción de la revisora retomó un objetivo antiguo; el registro, rol y próxima entrega permitieron recuperación dirigida. [Incidente](../../04-operacion-agentes/evidencias/capacidad-audiovisual-001/incidente-contexto-v1.json). No hay compacción perfecta ni entrenamiento de modelos demostrado.
- Reutilizar un chat no cambia su LLM. ORQUESTACION ya exigía distinguir recomendado/solicitado/observado. Se conservaron antecedentes Astra/ultra; esta retoma local sí acreditó Sol medio por turn_context. [Evidencia](../../04-operacion-agentes/evidencias/capacidad-audiovisual-001/modelo-retoma-v1.json). La cuota es compartida, sin porcentaje atribuible por chat ni ahorro inventado.

La aplicación comprobada es una ficha con procedencia, cobertura y límites, controles finitos y detención ante fallo. No se repitieron suites/corpus, no se abrieron familias o servicios, ni hay operación 24/7 acreditada.

El siguiente paso corresponde a coordinación: retomar el cerebro existente con ASR, cortes/PTS y lecturas visuales verificadas, manteniendo OCR sólo auxiliar y audio semántico sin acreditar. Después se prepara el plan full Cloud. La ruta modular de este Cormac está ejecutada y cerrada; no se inician más motores o ensayos automáticamente. El fallo de este runtime/configuración no demuestra imposibilidad general. Este laboratorio no es una migración. La asignación se libera al cerrar y no quedan nuevos ensayos activos. La capacidad audiovisual integral permanece pendiente, sin otro intento automático.


## Cierre posterior: PANNs, 6 de noviembre de 2026

La prueba PANNs terminó y fue revisada: seis inferencias offline, dos controles conocidos del generador y cuatro ventanas que cubren los 37,78 s de audio del remux Cormac; 0 s visuales. Los criterios pareados congelados distinguieron voz de ceros y del silencio final. En Cormac, Speech supera Music en las cuatro ventanas; son scores sin umbral calibrado, no probabilidades ni prueba de ausencia de música.

Dictamen: señal auxiliar experimental de actividad de habla en estas entradas. No detector validado, efectos, límites exactos, palabras, emoción/prosodia, mezcla, sincronía o percepción integral. Grid 10 ms interpolado. CPU1/AS3 GiB, máximo 27,13 s por entrada y RSS máximo muestreado 1.267.875.840 B; limpieza comprobada. La revisión anterior de cero inferencias correspondía al bloqueo previo, superado sin alterar sus evidencias.

[Resultado breve y límites](PANNs-RESULTADO.md) · [Recibo final](panns-cloud-setup-v3/final-result.json) · [Revisión](../../04-operacion-agentes/evidencias/capacidad-audiovisual-001/panns-revision-v1.json). Exportes locales 21/21 verificados; ZIP de curvas completas sólo en laboratorio Cloud, sin publicación ni garantía de persistencia permanente. Prueba cerrada; audiovisual integral pendiente. No nuevos ensayos ni trabajo sobre cerebro/Cloud en esta unidad.
