# Contrato con el panel existente

`estado-fabrica.json` usa el esquema `onia-fabrica-estado-v1`, productor `automatizaciones`, ID del encargo y estado descriptivo `para_revision`. Fuente, pasos, entregables y evidencias son rutas relativas a base-operativa, exclusivamente bajo esta entrega. `pendientes` identifica entrada, responsable y siguiente acción. No representa aceptación, integración ni estado canónico del harness.

`contrato-canales.json` (`onia-meta-canales-v1`) detalla cuatro canales, modo simulación, comprobaciones locales, evidencia, entradas faltantes y aprobación pendiente. `listo=false`, `e2e_real=false`, `envios_reales=0` y `conector_real_habilitado=false` son invariantes de esta versión. No contiene credenciales, destinatarios ni mensajes privados.

El lector de operación admite la raíz exacta de esta entrega como productora de automatizaciones. La configuración de cada instancia incluye su ruta de export de forma explícita. El script de comprobación carga el export en una instancia aislada del lector y valida la presencia de evidencias y pendientes.

```bash
python3 -B _investigacion-onia/base-operativa/05-herramientas/fabrica-onia/3-automatizaciones/meta-canales-20261111/puente_panel.py
```

Para comprobar un despliegue, incluir la ruta exacta en `--estado`, verificar que la fábrica muestra los pendientes y cotejar las respuestas del servicio. Los estados describen el ensayo y las dependencias de cada canal. Las evidencias históricas conservan el rechazo del lector anterior.

El registro del harness aceptó el paquete de simulación en r33, con dictamen bueno sobre `61462714`. La admisión del export no cambia los bloqueos externos de cada canal.
