# Conexión del perfil de análisis a Codex

Fecha de comprobación: 2026-11-08T23:11:02-04:00. Sergio informó Google, Instagram y Facebook secundarios creados y autorizó conectar/probar el navegador, retomar investigaciones y medir varias sesiones. No incluye mensajes, publicaciones, producción, n8n ni gasto adicional.

## Comprobado

- Playwright MCP 0.0.84 y Chromium instalados se reutilizan. `browser-vps.py mcp --urls ARCHIVO` toma el préstamo exclusivo del perfil por `visor.lock`, cierra sólo la ventana Chromium registrada y mantiene Xvfb, VNC y web. Usa el mismo perfil privado, sandbox y pipe CDP; no publica un puerto CDP TCP.
- `codex-con-cuentas.py` configura sólo esa invocación de Codex, sin cambios globales. El filtro acepta únicamente navigate/snapshot/close y URLs HTTPS exactas en un archivo propio0600. Snapshot no admite filename y sólo se entrega después de navegación aprobada; no se reenvían metadatos adicionales ni títulos de otras pestañas. No hay herramienta de clic, escritura, evaluación de código o captura en este perfil.
- Prueba integrada sintética aprobada: persistencia de localStorage y cookie HttpOnly ficticia humano→MCP→humano, renderer Seccomp2/NoNewPrivs1, exclusión, entradas rechazadas, EOF/SIGTERM/SIGKILL y recuperación. También se comprobó reentrada desde `recuperar` y rechazo si el PID no coincide con SingletonLock. Los fixtures mantienen sus archivos y usaron marcadores de VNC/web; la prueba real siguiente sí usa el visor existente.
- Prueba NATIVA en el harness: `investigacion-acceso-av-20261108`, mismo SID `01a1bd30-efe1-7f90-b6e0-811def9bf063`, leyó example.com y perfil público de Heras, vio links de piezas y cerró el navegador. Cinco llamadas completadas. [Entrega publicada por la ejecutora](https://github.com/oninteligenciaartificial/onia/blob/8e347793e6032729c88d757444bccc846e52c542/_investigacion-onia/base-operativa/05-herramientas/acceso-av/20261108/PRUEBA-PERFIL-CUENTAS.md). Es evidencia de acceso al contenido público; no una auditoría de identidad/autenticación de cada cuenta.
- El coordinador comprobó el Chromium humano restaurado vivo y los mismos PID de Xvfb/VNC/web. La etiqueta quedó transitoriamente en `recuperar`, conciliada sin relanzar el navegador. La reentrada ya cubre ese caso conservadoramente. Las capturas anteriores y los perfiles se preservan fuera de Git.

## Uso y recuperación

La lista de destinos debe ser un archivo privado del usuario, con una URL HTTPS exacta por línea, sin query ni fragmento. Sólo el coordinador mantiene esa lista para la tarea autorizada. `ONIA_BROWSER_URLS_FILE` señala la ruta absoluta al invocar `codex-con-cuentas.py`; el harness puede usar el wrapper en el PATH de su supervisor, manteniendo `reanudar`, su SID, modelo y permiso Git privado. No se cambian config.toml ni el app-server.

```bash
python3 -B ~/repos/onia-coordinador/_investigacion-onia/base-operativa/05-herramientas/cuentas-analisis/20261108/browser-vps.py estado
python3 -B ~/repos/onia-coordinador/_investigacion-onia/base-operativa/05-herramientas/cuentas-analisis/20261108/browser-vps.py recuperar
```

Consultar PID desde el host, no inferir muerte desde un namespace del sandbox que no lo ve. `recuperar` exige lease libre y no abre otra instancia si el perfil sigue ocupado. No borrar SingletonLock ni matar el PID inferido de ese enlace. Un cliente que cancela una llamada sin respuesta debe cerrar su sesión MCP para devolver el préstamo; no superponer solicitudes.

## Límites y reversión

El filtro limita destinos y salidas para un agente confiable; no convierte el navegador en una API con permisos de sólo lectura. El navegador puede efectuar redirecciones y cargar subrecursos antes del cotejo final. Por eso cada tarea debe usar fuentes públicas concretas y no entrar en feed, correo, mensajes, ajustes ni perfiles propios. Un worktree no aísla una cuenta externa.

La consulta de YouTube que pidió Sergio contiene query y no forma parte de este piloto de dos destinos. Tampoco se probó Facebook. No se exportaron cookies, inspeccionó recuperación ni se publicaron DOM completos. Autenticación de cada servicio, reproducción audiovisual y nuevos destinos requieren su comprobación, no se deducen de un perfil abierto.

Para retirar esta integración: cerrar primero la sesión MCP propietaria, comprobar procesos y usar `recuperar` si corresponde; dejar de inyectar el wrapper. Esto conserva cuentas, perfil, visor y código. El gestor anterior está respaldado privadamente bajo `~/operacion/cuentas/analisis-onia/versiones/20261109T025453Z/`; no reemplazar código ni perfil mientras exista un propietario activo. Git conserva la versión anterior. No se toca AppArmor, configuración global ni servicios de producción.

El scheduler y el aumento de concurrencia son otro alcance: siguen sólo como [propuesta pendiente](../../2026-11-08-harness/ESCALADO-CARRILES-PROPUESTA.md). El máximo actual sigue siendo tres sesiones principales por registro de operación compartido; el navegador autenticado tiene un propietario a la vez.
