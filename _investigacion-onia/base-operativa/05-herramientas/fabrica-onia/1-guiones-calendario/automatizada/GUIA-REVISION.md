# Recorrido para Sergio y la coordinadora

La entrega es una tanda local verificable de **cinco guiones v3**, versión editorial **r2**, más un procedimiento invocable. Está preparada para revisión: sin aprobación editorial, publicación ni operación comercial acreditada. STOP después del commit/push de esta rama; no aceptar, integrar ni iniciar la siguiente tanda desde esta sesión.

## Qué abrir

1. [Tanda y duraciones estimadas](../salida/guiones-tanda-20261111-v3/README.md). Leer T01 venta, T02 marca, T03 anuncio fechado, T04 segunda venta y T05 prueba. Cada Markdown contiene voz, copy, propósito, fuentes, criterio y adaptación vertical/horizontal de la misma idea.
2. [Calendario](../salida/guiones-tanda-20261111-v3/CALENDARIO.md): clases viernes 13 20:00, sábado 14 14:00 y lunes 16 20:00, America/La_Paz; sin hora final ni publicación fijada. Es archivo local; Calendar no fue consultado ni modificado.
3. [Fuentes](../salida/guiones-tanda-20261111-v3/FUENTES.md) y [selección trazable](../salida/guiones-tanda-20261111-v3/seleccion.json). El cerebro y la v2 se reutilizan en lectura. Noticia: primaria publicada el **10-nov-2026**, consulta fechada en fuentes.json, anuncio sin demo propia. No se presenta como hecho del 11. Se descartó el anuncio de búsqueda web de marzo de 2025 por antigüedad. No hubo ASR nuevo, capturas ni investigación de audiencia.
4. [Corrección C01](../salida/guiones-tanda-20261111-v3/correcciones-aplicadas.json): de r1 a r2, seis campos de T01/T04. Se quita «te paso la información» y se deja una invitación a comentar, porque la atención real de NEGOCIO no está probada. El canal sigue bloqueando publicación. La corrección propuesta por el productor no es aprobación de Contenido.
5. [Paquete compatible](../salida/guiones-tanda-20261111-v3/guiones-panel.json), [recibo de integridad](../salida/guiones-tanda-20261111-v3/recibo.json) y [resumen de fábrica](../salida/guiones-tanda-20261111-v3/estado-fabrica.json). Sus hashes acreditan bytes, no aceptación; el resumen no muta el harness.

## Comandos y resultados reales

Ejecutados desde este worktree, base inicial `7012ca493bfd059a833b8a6cdd77b080b38765d8`, rama `codex/ws-guiones-tanda-automatizada-20261111`. Lecturas de arranque explícitas: AGENTS, BITACORA-BOSS, DECISIONES, ESTADO, reglas-comunes, boss-memoria, ORQUESTACION, orquestacion.json, arquitectura, directora desarrollar-y-verificar y ALCANCE-v1. El alcance local se cotejó sin diferencias con `origin/master`. Catálogo nativo recibido: incluye desarrollar-y-verificar; cuerpo leído desde su fuente canónica, enlace local presente. ONIA como inicio automático no acreditado. Briefing recibido en el mensaje de entrada, sin exigir un archivo local ni reconstruir su proyección. No se consultó/mutó el registro canónico del coordinador.

```bash
A=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/1-guiones-calendario/automatizada
O=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/1-guiones-calendario/salida/guiones-tanda-20261111-v3
C=_investigacion-onia/base-operativa/03-referentes/cerebro-operativo/20261109
python3 -B "$C/consultar.py" validar
python3 -B "$A/generar.py" \
  --brief "$A/entradas/brief.json" --fuentes "$A/entradas/fuentes.json" \
  --redaccion "$A/entradas/redaccion-r1.json" \
  --correcciones "$A/entradas/correcciones-r2.json" --salida "$O"
python3 -B "$A/comprobar.py" --salida "$A/evidencia/ensayo-v1"
git diff --check
```

Resultados del primer ensayo: cerebro íntegro, **28 fuentes / 19 referentes / 23 patrones**. Generación: código 0, cinco piezas, versión r2, seis cambios. **25/25 tests**, sin omisiones; `git diff --check` limpio. Evidencia guardada: [resultado.json](evidencia/ensayo-v1/resultado.json), [log de unittest](evidencia/ensayo-v1/unittest.txt). Los destinos de los dos comandos que escriben ya existen: repetir esos comandos exactos los rechaza; para revisar de nuevo seguir los comandos de reproducción del README usando nombres nuevos. No borrar ni forzar salidas para repetir.

La demostración generó dos salidas locales r1 y r2 en temporales propios dentro de v3, conservó los hashes de r1 y aplicó C01 en r2. Los cinco Markdown de r2 coincidieron byte por byte con la entrega raíz. Después retiró sólo esos temporales. La evidencia conserva huellas de ambas salidas, cambios y errores. El CLI real devolvió código 2 para propósito ausente, idea duplicada y destino ocupado, sin crear salida inválida ni pisar r1. También se prueban fechas ausentes/obsoletas, fuente secundaria/alterada, CTA discrepante, variante ausente, corrección de otra entrada, ruta histórica y enlace de salida.

Compatibilidad: **`tanda.snapshot` y `panel.render` reales, sin cambios**, recibieron T01–T05 y devolvieron los cinco títulos en HTML, con revisión técnica `null`; una alteración de Markdown en un temporal fue rechazada por hashes. Las huellas de tanda.py/panel.py/lector.py se cotejaron con HEAD. El render se hizo en memoria, sin escribir en la ruta asignada al panel ni realizar prueba de navegador.

## Límites que la revisión debe resolver

- El consumidor rotula toda tanda como «tanda v2». Los datos adicionales `version_editorial=r2` y los encabezados Markdown identifican esta v3; aquí no se modifica el panel ajeno. Fuentes y calendario se entregan como archivos, sin afirmar su incorporación a nuevas secciones de UI.
- Duraciones por palabras: T01 47–63 s, T02 38–50 s, T03 38–51 s, T04 43–57 s, T05 35–47 s. Fórmula: 115–150 palabras/minuto, sin pausas/tarjetas medidas; **hasta ensayo humano**. No hay grabación ni montaje realizado.
- La voz, selección, ideas y juicio sobre fuentes provienen del LLM de esta sesión. Python aplica reglas fijas y correcciones literales. No hay llamada a modelo, red ni scheduler dentro del generador. Ningún procedimiento guardado garantiza noticias/redacción/operación después del 14; necesita redactor/modelo y operador efectivamente disponibles.
- Solicitado: Sol6.1 high, sin hijos. Modelo/esfuerzo efectivos y cuota inicial/final no observables desde estas herramientas: **desconocidos**, no inferidos del briefing. Una sesión de ejecutor observada; intentos canónicos no consultados. Ensayo local correcto; revisión independiente/editorial pendientes.
- Personas y crítico son hipótesis del productor. T05 carece de respuestas reales y ganador; sólo propone medir claridad percibida. No hubo investigación de audiencia, ventas ni conversión observada. Duplicados semánticos y verdad de cualquier redacción futura necesitan revisión humana.
- Falta relato real de Sergio: tarea de hoy, entrada saneada, borrador, error, corrección y permiso. T02 construye marca con un ejemplo escrito ficticio, sin autobiografía falsa. No bloquea entregar este borrador; bloquea presentarlo como vivencia real.
- NEGOCIO y todo el recorrido comercial requieren prueba real por Operaciones/Sergio antes de publicar. QR y seguimiento, confirmación manual de cada pago por Sergio; captura sola no confirma inscripción. No se incluyeron secretos, QR, clientes ni enlaces privados. No se activó n8n, calendario real, servicio, modelo descargado, pago, PC o publicación. El vlog queda excluido.

Siguiente responsable: la coordinadora cierra conservando trabajo y prepara la revisión solicitada; Contenido/Sergio revisan texto y ensayo, Operaciones prueba el canal bajo autorización aplicable. La aceptación técnica posterior corresponde a una sesión distinta sobre el commit entregado. Este productor termina con su commit/push y STOP.
