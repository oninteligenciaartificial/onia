# Corrección de la revisión independiente

Dictamen recogido: cambios sobre fb86bb2. Se reprodujeron P1 y P2; no se aceptó ese commit.

P1 corregido: el resultado se identifica por contenido y commit. Cada tick coteja la entrega canónica, vuelve a validar/leer sus artefactos cuando cambia y sólo asocia un dictamen si su commit coincide con el resultado. Se conservan las versiones anteriores. Una entrega nueva inválida conserva el texto previo, retira la revisión heredada y muestra resultado_invalido.

P2 corregido: la proyección valida todos los campos consumidos por la vista y por attach antes de sustituir la caché. Falta de huella, generado, versión o versión editorial conserva la última página válida; se probó HTTP200 y aviso de actualización fallida.

35 pruebas de ciclo/programación y 5 HTTP correctas; comandos, salidas y hashes en evidencia/coordinadora-v2. Las 25 pruebas del generador constan en evidencia/coordinadora y su archivo no cambió. Navegador de host anterior en evidencia-visual-host-02: no se atribuye un nuevo recorrido visual a las correcciones P1/P2, comprobadas por HTTP y transición de estado.

La plantilla de servicio incorpora PATH del Codex instalado y KillMode=process para que el disparador no mate las supervisoras administradas por el harness al salir. Está documentado y no se instaló ni activó; la prueba real del timer queda pendiente de autorización. No se cambió el harness.

Falta recoger una nueva revisión del commit corregido antes del ensayo real y de cualquier integración del flujo.
