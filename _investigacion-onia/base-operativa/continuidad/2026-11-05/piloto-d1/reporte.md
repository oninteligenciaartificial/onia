> Entrega fechada conservada íntegramente salvo enlaces ajustados. Procedencia local: `operacion/piloto-d1-local/reporte.md`; SHA-256 del original: `38681daa1268f1cc4c2fd0ce629226215609609139cbbf511bc0bd4e94c25237`. Sus pausas, responsables y próximos pasos describen ese corte; el alcance vigente está en [HANDOFF-JEFA.md](../HANDOFF-JEFA.md). Esta copia versionable conserva el contexto; el original ignorado no es autoridad operativa.

**D1 · animatic privado SILENCIOSO · 5 de noviembre de 2026, America/Caracas**

Resultado: MP4 real producido y verificado. Nueva composición de tarjetas basada en el [brief aprobado](../d1-piloto.md); no procede del ZIP cloud. Es una prueba hipotética sin rostro, voz, música, SFX ni publicación. El audio continúa fuera de alcance y no está solucionado.

| Entrega | Archivo |
|---|---|
| MP4 final | [d1-piloto-silencioso.mp4](../../../operacion/piloto-d1-local/d1-piloto-silencioso.mp4) |
| Editable | [index.html](index.html), con `assets/` locales; [configuración](hyperframes.json) y [ejecutor](run.mjs) |
| Contacto del MP4 | [contacto-visual.jpg](../../../operacion/piloto-d1-local/contacto-visual.jpg); [fotogramas individuales](../../../operacion/piloto-d1-local/fotogramas) |
| Evidencia | [verificacion.json](verificacion.json), [metadata.json](metadata.json), [decodificacion.log](decodificacion.log), [check.log](check.log), [render.log](render.log), [hashes](sha256.json) |

**Resultado técnico.** 1080×1920, H.264/yuv420p, 24 fps, **43,000 s / 1.032 fotogramas**, 385.060 bytes y **cero pistas de audio**. Decodificación completa con FFmpeg, `-xerror`, salida 0. SHA-256 MP4: `c41798b0c33c1d42232aba8a542696748b548b1ba327560d3ff148edc5f1c71c`.

**Comando ejecutado**, desde `C:\dev\proyectos\_investigacion-onia\base-operativa\operacion\piloto-d1-local`:

```powershell
node run.mjs render --output d1-piloto-silencioso.mp4 --fps 24 --quality standard --workers 1 --low-memory-mode
```

Motor existente HyperFrames **0.9.9**, GSAP **3.15.0**, Chrome instalado; sin instalación/actualización. El ejecutor llama directamente al CLI fijado de la caché, sin npm ni descarga. Un render, un trabajador, captura por screenshot y modo poca memoria. Motor: **18,4 s**; comando completo: **21,071 s**, salida 0, según [registro de ejecución](render-result.json). Inicio 07:56:42 y fin 07:57:03, America/Caracas. Las fuentes locales se copiaron de Windows para esta pieza privada; GSAP procede de la prueba previa. No se modificó esa prueba ni se usaron Docker, WSL o VPS.

**Comprobación editorial/visual.** Tarjetas cotejadas literalmente con el brief, cinco tramos 0–8 / 8–18 / 18–27 / 27–37 / 37–43 s y un único CTA al final. Rótulos persistentes «EJEMPLO HIPOTÉTICO» y «ANIMATIC SILENCIOSO · PRUEBA PRIVADA». La ficha aparece a los 2 s; el borrador entra completo, sin simular generación. Se mantiene el mismo verde en ambas fechas de la comparación y se subraya la segunda frase de la instrucción.

HyperFrames revisó 11 tiempos: cero errores de runtime/layout; **29/29 contrastes** aprobados. Conserva seis avisos de estructura: cinco escenas anidadas y densidad de una pista; no bloquean el render. La comprobación automática de motion no estuvo habilitada. Extraídos 11 PNG del MP4; inspeccionados visualmente inicio, las cinco escenas y final en contacto/imagen. Textos completos, sin recortes ni solapamientos visibles en esas muestras. No se presenta como visionado humano continuo.

**Incidencias resueltas.** El primer check restringido falló por acceso al servidor local y escritura de historial; se usó la escalación autorizada y se alojó historial/caché temporal dentro de `.work/`. Una referencia de fuente ausente se resolvió copiando el archivo instalado correcto, sin instalarlo. Se conservan `check-sandbox-failed*` y `check-font-failed*`; el check final pasó. No se desactivaron controles de seguridad.

**Revisión pendiente:** Jefa revisa el MP4 a velocidad normal y registra si puede explicar, sin ayuda, que la fecha falta y que «viernes» sólo proviene de la pregunta. La lectura real, comprensión y aprobación editorial quedan pendientes; no se atribuyen retención, ventas ni calidad vocal a esta prueba.


**Consolidación del 5/11:** textos técnicos incorporados sin cambiar lógica ni ejecutar el paquete. [Dependencias y procedencia](REPRODUCIBILIDAD.md). Los logs check/render conservan resultados y advertencias, con progreso/trazas repetitivas omitidos y hash del original en cabecera/manifiesto. MP4, fotogramas, tipografías, dependencias y `.work` no se copiaron. Esta copia **no se probó como paquete portable**. La aprobación editorial posterior comunicada por la jefa se limita a prueba silenciosa; comprensión humana, locución y retención siguen pendientes.
