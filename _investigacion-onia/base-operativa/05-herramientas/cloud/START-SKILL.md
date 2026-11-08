# Instrucción de inicio del entorno onia

Trabajar desde /workspace/onia. Antes del encargo, leer AGENTS.md y seguir _investigacion-onia/base-operativa/05-herramientas/cloud/INICIO-SESION.md, que remite a las reglas, estado y selección de skill. No cargar todo el historial.

Confirmar repo, HEAD y cambios. Registrar si la entrada y las skills ONIA estaban anunciadas en el catálogo inicial; distinguirlo de archivos descubiertos y leídos después. Seleccionar directora por orquestacion.json y leer su fuente aunque no aparezca nativamente. Si se recibió un ID/commit, recuperar el registro conforme a cloud/CONTINUIDAD.md sin descartar trabajo existente.

Desde /workspace/onia, comprobar enlaces con `python3 _investigacion-onia/base-operativa/05-herramientas/scripts/preparar-cloud.py --check --discovery-root /workspace` y rutas con `python3 _investigacion-onia/base-operativa/05-herramientas/scripts/harness.py doctor`. Ejecutar tests cuando el encargo cambie código o deba validar el setup; no reinstalar dependencias en cada inicio. Iniciar navegador o consultar cuentas sólo si hace falta para el trabajo autorizado, siguiendo cloud/OPERAR.md.

No exponer secretos ni trasladar sesiones autenticadas. Conservar una entrega saneada recuperable y registrar pruebas/límites en el lugar autorizado por el encargo. Un registro local ignorado no se comparte por Git y una lectura por archivo no acredita descubrimiento automático.
