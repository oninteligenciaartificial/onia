# Cormac Hayden · agentes con acceso al escritorio

Recibido de Sergio el 5 de noviembre de 2026. ID: `DfWLWspIruU`. **Estado: referencia; adaptación por probar. Análisis parcial, sin cierre audiovisual integral.**

## Fuente y cobertura

- [Reel exacto](https://www.instagram.com/reel/DfWLWspIruU/), cuenta `cormachdn`, nombre devuelto por metadata: Cormac Hayden. Descripción: propone instalar agent-desktop, conectarlo a contexto local en `@askhalos` y aportar una lista de tareas. Identidad del producto Halos no corroborada mediante documentación propia accesible.
- Medio recuperado públicamente con yt-dlp, sin cookies ni login. Ruta auxiliar: `operacion/reels-e-ideas/DfWLWspIruU/DfWLWspIruU.mp4`, relativa a la base. SHA-256: `9be4267480093249e104ec9821271e1a755e4329b7ea4d8fca3fc8bacd3b664e`. Duración técnica 37,754 s; 1440×2560, VP9 y AAC 44,1 kHz. Metadata original en la misma carpeta; no se copia a esta ficha.
- Inspección de 38 muestras visuales a 1 Hz distribuidas por la pieza: hojas `contacto.jpg` (25 muestras) y `cierre.jpg` (13 desde el segundo 25). Texto visible examinado en esas imágenes; no lectura certificada de cada subtítulo ni de detalles pequeños de todas las ventanas. No visionado continuo ni medición de transiciones/movimiento.
- ASR sobre la pista completa: faster-whisper small, pesos locales existentes, CPU int8, cuatro hilos, inglés, VAD, sin descarga de modelos ni API paga. Salida en `asr.json`, audio mono 16 kHz en `audio.wav`, ambos auxiliares. Sus 18 segmentos cubren de 0 a 37,84 s; el último tiempo automático excede ligeramente la duración técnica. ASR es contenido verbal candidato, no escucha ni certificación de palabras, prosodia o sincronía.
- Voz/prosodia, música, efectos, ambiente, silencios perceptuales y mezcla **sin evaluar**. Las pruebas acústicas/temporales previas siguen rechazadas según [estado operativo](../../00-MAPA/ESTADO.md); no se repiten ni se aplica un modelo fallido. Sin Higgsfield. La recuperación inicial falló por DNS en sandbox; la lectura pública con red autorizada funcionó. El lector web devolvió cache miss y búsqueda por ID sin resultados.

## Qué hace la pieza

Tiempos aproximados, guiados por ASR y muestras:

| Tramo | Observación y función inferida |
|---|---|
| 0–3,5 s | Presentador con micrófono de mano y subtítulos blancos; apertura que cuestiona por qué seguimos trabajando. Hipótesis: despertar curiosidad mediante una promesa amplia. |
| 3,5–7,2 s | Inserto del escritorio con varias aplicaciones, calculadora y listas. El autor afirma haber dado acceso al equipo para delegar tareas. La simultaneidad visible no prueba coordinación ni resultados. |
| 7,2–14,6 s | Cámara dirigida al repositorio agent-desktop y su documentación; señala la pantalla. Aporta una referencia técnica comprobable, pero no muestra instalación y ejecución completas. |
| 14,6–35 s | Regresa al presentador. Explica la combinación con su sistema Halos, datos personales, pendientes y mensajes. Son afirmaciones de su operación; el reel no permite auditar memoria, permisos, exactitud o envíos. |
| 35–37,75 s | Cierra con otra pregunta sobre dejar de trabajar. No se observa placa final de compra; la descripción contiene los pasos técnicos. |

La alternancia entre cara, escritorio y repositorio conecta persona, promesa y herramienta. Los subtítulos cortos permiten seguir fragmentos verbales. Las muestras sugieren pocos bloques grandes; no permiten juzgar ritmo sonoro o calidad de los cortes. No se midieron retención, ahorro, costo ni éxito real de tareas.

## Contraste técnico y aplicación a ONIA

[Documentación oficial consultada](https://github.com/vercel-labs/agent-desktop): CLI/C library que expone aplicaciones mediante accesibilidad; el modelo y el bucle de decisión pertenecen al agente externo. La documentación declara soporte Windows, macOS y Linux. [Instalación oficial](https://github.com/vercel-labs/agent-desktop/blob/main/docs/install.md) exige comprobar plataforma/permisos; no se instaló ni probó aquí. `Get-Command agent-desktop` no devolvió un comando disponible en esta sesión: sólo acredita ausencia de resolución en PATH, no ausencia absoluta del equipo.

**Qué tomar:** contexto pertinente + tarea acotada + operación observable + comprobación del resultado. ONIA ya conserva contexto y responsables en el repo y dispone de herramientas de escritorio anunciadas en esta sesión; su existencia no acredita una ejecución. El aporte es escoger una tarea útil y medir el recorrido.

**Qué evitar:** equiparar abrir ventanas con completar trabajo o prometer que puede resolver cualquier tarea. Tampoco trasladar toda la información personal a otra plataforma por imitación. El acceso a escritorio no crea por sí mismo memoria, scheduler o autorización para mensajes.

Comparación: comparte con [Alex Carrera y Voltra](../../03-referentes/fichas/audiovisual/LECTURA-COMPARADA.md) mostrar pronto un objeto concreto. Aquí falta una prueba legible del resultado final; una pieza propia de ONIA puede mejorar justamente eso. El [piloto D1 existente](../d1-piloto.md) ya ofrece un caso y una regla de cotejo verificables.

## Cambio propio preparado: ensayo de escritorio con D1

**Hipótesis:** usar contexto mínimo y verificar el archivo final permite delegar una tarea pequeña sin inventar la fecha ni confundir borrador con envío. Responsable propuesto: Desarrollo para una prueba acotada cuando Jefa la priorice; este chat conserva análisis y resultado. No se despachó ni activó esa prueba.

Instrucción de ensayo lista para usar con las herramientas ya disponibles, sin requerir instalar agent-desktop:

> Abrí una copia de prueba de la ficha D1 en un editor local. Con la fecha por confirmar y la consulta «¿Es este viernes?», creá un borrador en una carpeta de prueba exclusiva. Conservá explícito que falta confirmar la fecha. Volvé a abrir el archivo guardado y cotejá el texto con la ficha. Entregá ruta, resultado del cotejo, tiempo e intervenciones necesarias. El destino es sólo ese archivo local.

**Aceptación:** archivo recuperable y releído desde la aplicación; fecha pendiente preservada; cero datos añadidos sin respaldo; tiempo e intervenciones registrados; evidencia del antes/después. Si la interfaz falla, registrar el paso exacto y el costo de recuperación. La prueba posterior podrá justificar comparar otra herramienta sólo si identifica una limitación concreta de la actual.

**Resultado hoy:** análisis y ensayo propuesto escritos, descarga y ASR ejecutados; ensayo de escritorio, aprendizaje humano y ahorro todavía no probados. No cambia prioridades ni implementa producto/automatizaciones.

**Brecha con salida:** para completar la evaluación perceptual hace falta una capacidad que supere los controles existentes o una revisión humana delimitada de este archivo. Revisión acústica sugerida a Sergio si quiere completar esa dimensión: 0–7,2 s (voz y fondo), 7,2–14,6 s (cambio sonoro durante pantalla), 35–37,75 s (pausa y cierre); el resto conserva su pendiente. Pregunta: ¿hay música o efectos, cómo cambian y qué pausas destacan? Una respuesta sólo acredita los intervalos revisados. Responsable técnico del desbloqueo general: Jefa/Video/Desarrollo conforme al estado vigente; este chat retoma la ficha al disponer de evidencia nueva.
