# Pruebas reproducibles

Ejecutar desde la raíz del checkout, sin instalar dependencias:

```bash
M=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/3-automatizaciones/meta-canales-20261111
python3 -B "$M/ensayo.py"
python3 -B "$M/puente_panel.py"
python3 -B -m unittest discover -s "$M" -p 'test_*.py' -v
git diff --check
```

No se inicia un servidor ni se llama a Meta/n8n. El ensayo usa reloj fijo del 11-nov y vuelve a abrir SQLite; nunca toma la fecha actual para fingir vigencia. Las pruebas cubren los cuatro canales y éxito/rechazo/timeout/resultado incierto, además de firma, challenge, identidad, duplicados, colisiones de ID, concurrencia, reinicio, baja, orden tardío, caducidad local, inyección, privacidad, destino, oferta y consumo del panel. Los archivos SQLite están en directorios temporales privados fuera del repo.

Evidencia vigente de la corrección P2: `evidencia/correccion-p2/pruebas-final.txt`, `evidencia/correccion-p2/recorridos.json`, `evidencia/correccion-p2/panel.json` y `evidencia/correccion-p2/comprobacion.json`. Los archivos anteriores de `evidencia/` se conservan íntegros como prueba histórica del commit `612a99b`; sus hashes no se actualizan para atribuirles la corrección. Sólo es simulación local y lectura de contrato; ninguna salida equivale a un mensaje real. El lector sin puente rechaza el productor; el puente local comprueba el esquema sin publicar UI. La prueba real autorizable queda en ACTIVACION-PENDIENTE.md.

Resultado de la versión corregida: **44 pruebas, todas correctas**, sin omisiones. El caso de transporte recorre 16 combinaciones (cuatro canales por cuatro resultados ficticios). El ensayo público conserva cuatro recorridos completos: información, repetición, reinicio, destino ausente, derivación con destino ficticio privado y baja; luego 16 recibos de transporte, todos con cero envíos reales y sin reintento terminal. La suite comprueba ese reporte y la ausencia de destino/secretos en su JSON.

P2 se reprodujo en los cuatro canales sobre `612a99b`: evento preparado un segundo antes del vencimiento, oferta ya inválida al consumirlo y resultado incorrecto `exito_simulado`. La reproducción queda en [reproduccion-612a99b.json](evidencia/correccion-p2/reproduccion-612a99b.json). Las cinco regresiones nuevas ejecutadas antes de corregir produjeron 20 fallos de subcasos; su salida íntegra y SHA256 están en [regresiones-antes.json](evidencia/correccion-p2/regresiones-antes.json). Se pueden ejecutar por separado con:

```bash
python3 -B -m unittest discover -s "$M" -p 'test_*.py' -k pending_offer -v
```

Ahora el consumo revalida vencimiento y hashes de las fuentes, incluso después de reabrir SQLite. Cambiar decisiones/catálogo, perder una fuente o corromper un JSON cancela el pendiente sin atribuirle éxito, rechazo o timeout de transporte. La cancelación es terminal y conserva `outcome=NULL`; la prueba incluye derivación a WhatsApp y una cola vacía que no consulta fuentes innecesariamente. Los archivos compartidos de negocio no se modifican durante estas pruebas: los cambios de fuente se simulan mediante mocks de lectura.

Salida resumida del consumidor real con puente:

```json
{
  "estado": "para_revision",
  "exports_consumidos": 1,
  "documentos": 12,
  "targets_revision": 11,
  "documentos_disponibles": true,
  "errores_modelo": [],
  "ui_publicada": false
}
```

| Criterio del encargo | Evidencia local |
|---|---|
| Recorrido y fallos por canal | `evidencia/correccion-p2/recorridos.json`: cuatro recorridos, 16 resultados ficticios; `test_four_channels_roundtrip_restart_and_all_transport_failures` |
| Identidad, inyección, orden tardío y baja por canal | `test_each_channel_late_injection_identity_and_baja`; baja tardía y comentario→DM con reinicio |
| Firma/challenge, límites y atomicidad | Rechazos de HMAC/payload/JSON/IDs, lote mixto sin efectos parciales, dos hilos duplicados |
| Timeout e incierto sin reintentos | Dos hilos despachan una salida; tras reiniciar no reaparece como pendiente |
| Información vigente y destino privado | Hashes de catálogo/decisiones, caducidad local, deriva/missing offer sin impedir BAJA, destino validado y ausente |
| Revalidación de pendientes (P2) | Cinco métodos `test_pending_offer_*`: vencimiento con evento de un segundo, cambio de fuente tras reinicio, fuente ausente/inválida, derivación y cola vacía |
| Contrato de panel y permisos pendientes | Consumo de `load_export`/`build` existentes, invariantes del contrato detallado; UI y E2E real permanecen falsos |
| Ninguna activación/envío/gasto | Sin transporte ni servidor; `RealConnector` rechazado bajo socket bloqueado, configuración true rechazada |

Retrabajo anterior conservado: `evidencia/pruebas-inicial.json` conserva en base64 los bytes íntegros y su SHA256 del registro que contiene el fallo inicial de inserción (cantidad de valores SQLite) y de export (evidencia `.py` no admitida por el lector). Se corrigió la sentencia con seis parámetros más NULL y se enlazaron documentos admitidos sin ampliar permisos del panel. `evidencia/pruebas-v1.txt` conserva las 35 pruebas anteriores al recorrido ampliado; `evidencia/pruebas.txt` conserva las 39 pruebas del commit revisado. Una prueba inicial del puente se hizo antes de crear el log final y mostró documentos ausentes; la evidencia de aquel commit se regeneró después de disponer de todos los documentos. Ninguna de esas pruebas históricas valida por sí sola la corrección P2.
