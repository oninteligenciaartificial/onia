# Contrato con el panel existente

`estado-fabrica.json` usa el esquema `onia-fabrica-estado-v1`, productor `automatizaciones`, ID del encargo y estado descriptivo `para_revision`. Fuente, pasos, entregables y evidencias son rutas relativas a base-operativa, exclusivamente bajo esta entrega. `pendientes` identifica entrada, responsable y siguiente acción. No representa aceptación, integración ni estado canónico del harness.

`contrato-canales.json` (`onia-meta-canales-v1`) detalla cuatro canales, modo simulación, comprobaciones locales, evidencia, entradas faltantes y aprobación pendiente. `listo=false`, `e2e_real=false`, `envios_reales=0` y `conector_real_habilitado=false` son invariantes de esta versión. No contiene credenciales, destinatarios ni mensajes privados.

Consumidor inspeccionado: `05-herramientas/fabrica-contenido/20261109-lector-panel/operacion.py`, HEAD base `de1d9ab8b31b62c47b4f4455b7e7ab0d930b3b6c`. Reconoce la fábrica visual `automatizaciones`, pero su lista `PRODUCERS` admite guiones, WhatsApp y panel. **La UI existente rechaza este productor sin puente.** No se editó el panel ni su configuración de despliegue.

`puente_panel.py` importa una instancia aislada del lector y comprueba primero ese rechazo. En esa instancia añade explícitamente la raíz de esta entrega a `PRODUCERS['automatizaciones']`; invoca `load_export` y `build` reales y comprueba que la fábrica recibe un export con documentos disponibles. No escanea otras carpetas ni modifica el módulo del panel en disco. Su salida JSON es una comprobación local del contrato, no publicación de UI. Una instancia nueva del lector conserva su lista original; la suite lo verifica.

```bash
python3 -B _investigacion-onia/base-operativa/05-herramientas/fabrica-onia/3-automatizaciones/meta-canales-20261111/puente_panel.py
```

Integración pendiente para el único escritor del panel: incorporar explícitamente esta raíz a la lista de productores, incluir la ruta exacta de `estado-fabrica.json` en su lista de exports, consumir los cuatro registros del contrato detallado si quiere mostrarlos por canal y probar UI escritorio/móvil con pendientes/error/revisión. No otorgar permisos de envío por leer un export. La prueba local actual acredita lectura del esquema por el consumidor; no acredita UI ni servicio desplegados.
