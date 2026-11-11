# Pruebas del flujo

Ejecutar desde la raíz del checkout con Python 3.10+ en Linux. Todo el trabajo de modelo/harness se sustituye por dobles controlados. No lanzar Codex ni APIs para reproducir estas suites.

```bash
B=_investigacion-onia/base-operativa/05-herramientas
F="$B/fabrica-onia/3-automatizaciones/flujo-diario"
python3 -B -m unittest discover -s "$F" -p 'test_*.py' -v
python3 -B -m unittest discover -s "$B/fabrica-contenido/20261109-lector-panel" -p test_diario.py -v
python3 -B -m unittest discover -s "$B/fabrica-onia/1-guiones-calendario/automatizada" -p 'test_*.py' -v
python3 -B "$F/programacion.py"
```

Última validación: `evidencia/validacion-v2/`. Las evidencias anteriores se conservan con sus hashes/fecha propios y no se presentan como validación del código posterior. No se repitieron las 55 pruebas históricas del panel.

| Componente | Resultado | Evidencia |
|---|---|---|
| Motor, fuentes, adaptador y programación | 28 pruebas sintéticas | validacion-v2/ciclo.txt |
| Integración nueva del panel por HTTP | 4 pruebas nuevas | validacion-v2/panel-nuevo.txt |
| Generador modificado, compatibilidad y consumidor | 25 pruebas | validacion-v2/generador.txt |
| Fuente real y repetición | Candidata fechada, un ciclo, cero lanzamientos | fuente-real-01.json |
| CLI sintético y disparo único | Recibos diferenciados, sin modelo real | validacion-v2/cli.json |
| Navegador con sandbox | No completado: Chromium no arrancó | ../evidencia-visual-01/resultado.json |

Cobertura del motor: entrada → candidata → pedido inmutable → registrar/asignar/lanzar → cierre remoto → resultado validado y ensamblado → revisión/recogida → proyección. Un segundo evento no duplica; los cambios de artículo conservan identidad por URL. Caídas antes/después del despacho se recuperan sin otro lanzamiento; envío incierto queda bloqueado. Se comprueban cambio de día La Paz, recuperación del archivo de pedido desde el journal, crítica y 20 candidatas, rechazo de fuentes ajenas, noticia inválida/error visible, modelo/permiso ausentes, tres cupos llenos, alcance/revisión obsoletos, versiones/corrección/originales y publicación atómica fallida.

El adaptador llama las APIs reales conocidas con dobles: `harness.prepare`, `trabajo.assign`, `harness_sesiones.launch/close/collect_review`; afirma revisiones, rutas, modelo high, auth ChatGPT y cero hijos. No se simuló una llamada de modelo como si fuera real. El registro canónico del encargo actual no fue leído/modificado por las pruebas; no se creó otra tarea real.

HTTP comprueba lectura del feed/guiones, POST real con Origin/Host/CSRF válidos, rechazo de Host/Origin/CSRF/huella y versión obsoletos, escape de HTML, ausencia de payload privado en la respuesta y revisión persistente tras reinicio, con original conservado. Actualización corrupta mantiene el último éxito y resultado sin renovar su fecha.

## Demostración sintética completa

```bash
python3 -B "$F/ensayo.py" --datos /tmp/onia-demostracion-sintetica-nueva
python3 -B "$B/fabrica-contenido/20261109-lector-panel/servidor.py" \
  --datos /tmp/onia-demostracion-revisiones-nuevas \
  --flujo /tmp/onia-demostracion-sintetica-nueva/panel.json --puerto 8765
```

El primer comando exige datos nuevos y declara `SINTETICO`. Ensambla textos fijos aportados al doble; no es una nueva redacción autónoma. Fecha sintética congelada y fuente ficticia rotuladas. El segundo abre un servidor temporal de loopback; detener con Ctrl+C. No se escribe la demostración ni sus revisiones privadas en Git.

## Navegador en host con sandbox

Intentado dentro del sandbox de esta ejecutora: Playwright y Chromium están presentes, pero `chromium.launch({chromiumSandbox: true})` devolvió `Chromium sandboxing failed`. Se detuvo el servidor del ensayo y se conservó la evidencia; no se desactivó ninguna protección. No se acredita refresco visual, móvil ni capturas nuevas en esta sesión.

La coordinadora puede ejecutar este script en un host cuyo sandbox de Chromium funcione, usando el mismo commit y una carpeta de evidencia nueva dentro de la entrega:

```bash
node "$F/visual-flujo.cjs" "$F/evidencia-visual-host-01"
```

Tercer argumento opcional: directorio del runtime Playwright con `node_modules/playwright` y `browsers/chromium-1252/chrome-linux64/chrome`. No instalar ni configurar servicios para esta prueba. El script mantiene `chromiumSandbox: true`, limita el navegador a loopback, prepara datos sintéticos fuera de Git, prueba un refresco real con formulario abierto, texto/CSRF/versión/huella conservados, fallo del export, guardado, reinicio y vista móvil/escritorio, y detiene el servidor en `finally`. Conserva los datos privados; escribe capturas sólo si el navegador funciona.

## Lo que sigue sin probar

Un recorrido de modelo real a través del harness, disponibilidad/cuota futura, revisión independiente de este commit, redacción y revisión editorial reales, utilidad/voz humana, acceso desde teléfono de Sergio, activación horaria, n8n, canales comerciales, publicación, cobro y operación persistente. La fuente real no prueba capacidades del producto anunciado. El ensayo autorizado para la coordinadora está en README; no ejecutar el adaptador real desde esta sesión ejecutora.
