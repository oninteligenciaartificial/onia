# Arranque de una sesión ONIA

Esta es la instrucción de inicio para el entorno cloud `onia`; no reemplaza las reglas comunes.

Registrar antes de explorar archivos si ONIA y la instrucción de inicio fueron anunciadas nativamente. La prueba del 6/11 no los recibió; la lectura explícita de esta entrada sigue siendo el mecanismo comprobado. No confundirlo con descubrimiento automático solucionado.

1. Confirmar checkout `/workspace/onia`, remoto `oninteligenciaartificial/onia` y HEAD. Leer `AGENTS.md`, `reglas-comunes.md` y `ESTADO.md` del checkout vigente. No reutilizar un resultado de otra VM como prueba de esta sesión.
2. Consultar `orquestacion.json`, identificar el área por el encargo y leer la skill directora pertinente. Cargar apoyos sólo si resuelven una parte concreta. No esperar que Sergio copie las instrucciones. Si el catálogo nativo no anuncia nuestras skills, aplicar su fuente canónica por archivo y distinguirlo del descubrimiento nativo.
3. Comprobar enlaces con `python3 _investigacion-onia/base-operativa/scripts/preparar-cloud.py --check --discovery-root /workspace`. El instalador prepara nueve enlaces en `.agents/skills` del checkout y nueve aliases en `/workspace/.agents/skills`, todos a la misma fuente. No reemplazar enlaces ajenos ni copiar cuerpos de skills.
4. Ejecutar el encargo y delegar partes independientes según ORQUESTACION.md. Comprobar una cuenta sólo cuando se necesite. Los secretos se obtienen de su integración o de Secretos de red del entorno; no se muestran ni se guardan en archivos de entrega.
5. Si se recibió ID/commit, comprobar y recuperar esa referencia Git conservando cambios existentes y ejecutar `harness.py retomar ID`; leer su alcance y próximo paso. Para compartir una tarea nueva usar el registro único de `cloud/CONTINUIDAD.md`, evidencia saneada y commit publicado. No afirmar persistencia compartida por escribir sólo en `operacion/`, que está ignorado. No publicar sin revisar el contenido de la entrega.
6. Si el encargo necesita navegador, usar `cloud/browser-runtime.cjs` y el procedimiento de `cloud/OPERAR.md`. La confianza de Chromium debe reconstruirse en un directorio temporal escribible con la CA oficial verificada; no heredar un arreglo de /tmp de otra tarea ni desactivar TLS. El módulo no conserva cuentas entre VMs.

La preparación del entorno debe guardar esta lectura como parte de la habilidad de inicio. Un texto versionado sin configurar el inicio no acredita que se ejecute. La prueba de aceptación de carga es una nueva sesión: registrar catálogo inicial, skill seleccionada y ruta leída antes de ejecutar su primer encargo.

El recibo de inicio distingue checkout/HEAD, enlaces comprobados, catálogo inicialmente observado, entrada recibida y fuentes realmente leídas. Para catálogo/recepción usar observado, no observado o desconocido según evidencia; no deducirlos de ready. No cargar todos los cuerpos de skills ni historial por costumbre.

La retoma vigente es breve por defecto: briefing único en tarea.briefing.contenido, decisiones vigentes y siguiente paso. Consultar --completo o historial ID --revision N cuando haga falta. Comprobar asignación, actor y revisión antes de mutar. El perfil LLM recomendado no cambia la configuración; registrar solicitado y observado por separado, sin completar lo desconocido.
