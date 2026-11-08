# Aceptación reproducible para una implementación posterior

8-nov-2026, America/Caracas. **Especificaciones propuestas; no ejecutadas.** No hay helper ni servidor nuevo que ejecutar hoy. Los únicos checks reales del análisis están en [EVIDENCIA](EVIDENCIA.md). Estos casos verifican comportamiento de acceso; no se propone probar escrituras en producción para demostrar su rechazo.

## Banco sin cuentas ni red de producción

El futuro encargo debe construir un adaptador HTTP falso en memoria y un servidor MCP de fixture por stdio, sin daemon. Respuestas JSON fijas, reloj controlado y una credencial ficticia no válida para ningún proveedor. Registrar cada intento saliente con método, alias de operación y recurso sintético; nunca cabeceras. Los fixtures deben representar las cinco APIs y tool catalogs de lectura/escritura separados. Esto permite demostrar bloqueo **antes** del envío y distinguir el rechazo del proveedor del rechazo propio.

Contrato propuesto del lector: éxito completo rc=0; autorización insuficiente rc=20; autenticación vencida rc=21; integridad/conflicto rc=22; operación prohibida rc=23; salida incompleta/cuota/timeout rc=24. Son convenciones nuevas pendientes de implementar, no códigos de Codex ni de proveedores. Cada resultado lleva estado, servicio, alias, completitud, hash si se materializó y diagnóstico saneado.

## Casos comunes

| ID | Preparación y pasos reproducibles futuros | Resultado exigido y evidencia | Estado |
|---|---|---|---|
| T01 éxito | Seleccionar alias fixture permitido; simular dos páginas con cursor; invocar lectura; validar contenido canónico y manifiesto. | rc=0, dos peticiones esperadas, ninguna adicional, hash recalculable, `complete=true`; sin tokens ni URLs firmadas en stdout/stderr. | No ejecutado. |
| T02 permiso insuficiente | Token ficticio válido sin capacidad requerida; backend devuelve 403. Repetir con 404 ocultando recurso y con recurso fuera de allowlist local. | rc=20; no ampliación de scopes, login ni lectura de recursos vecinos. Caso local: cero peticiones. 404 indica inaccesible/ausente, no certeza de inexistencia. | No ejecutado. |
| T03 token vencido | Backend devuelve 401; reloj marca vencido. Caso A sin renovación; caso B con renovación simulada que devuelve credencial nueva; caso C `invalid_grant`. | A/C rc=21 sin paquete válido nuevo; B una sola renovación y una sola repetición de lectura. Fallo repetido detiene; no bucle ni secreto en logs. No todas las credenciales admiten refresh. | No ejecutado. |
| T04 escritura prohibida | Solicitar create/update/delete/execute/activate/share y tool de escritura conocida. Intentar método libre, URL arbitraria, redirección y GraphQL mutation. | rc=23, cero solicitudes al backend. En Notion admitir sólo POST search/query explícitamente tipados como lectura; negar demás. MCP POST de transporte no es criterio suficiente. | No ejecutado. |
| T05 duplicado | Ejecutar dos veces mismo servicio/recurso/revisión/hash; recuperar checkpoint existente. Repetir con mismo ID y hash diferente. | Igual: un solo paquete canónico y recibo de reutilización; distinto: rc=22 y preservar ambos para conciliar. No atribuir idempotencia al harness. | No ejecutado. |
| T06 interrupción/recuperación | Cortar exportación tras página 1 y antes del rename atómico. Retomar con cursor y ETag/revisión estable; después variar revisión del origen. | Temporal no se acepta como completo. Continuación estable deduplica por ID y versión; origen cambiado exige reinicio consistente o resultado parcial explícito. No mezclar snapshots silenciosamente. | No ejecutado. |
| T07 límites y cuota | Simular 429 con Retry-After, timeout, JSON inválido, página >1 MiB y cursor cíclico. | Hasta dos retries de lectura dentro del presupuesto; corte rc=24 y cursor/completitud, sin aumentar cuota ni activar recarga. No procesar cuerpo truncado como JSON válido. | No ejecutado. |
| T08 fuente maliciosa | Fixture contiene instrucciones para revelar credencial, consultar URL distinta o escribir una página. | Contenido citado como datos; ninguna operación adicional. Verificar además secreto ficticio ausente del paquete/log. No es prueba general de inmunidad a prompt injection. | No ejecutado. |
| T09 integridad/caducidad | Alterar un byte y luego usar manifiesto caducado o sin productor conocido. | rc=22 para hash; caducado bloquea o requiere nueva lectura según contrato explícito. Hash correcto solo no autentica productor. | No ejecutado. |

## Cobertura por servicio

| Servicio | Fixture de éxito | Negativo específico y recuperación |
|---|---|---|
| GitHub | Archivo por SHA en un repo permitido; contenido esperado, sin búsqueda global. | Segundo repo no autorizado; 403 SSO/cuota clasificados aparte; 401 requiere custodio. Token de push nunca se consume como fallback. |
| Notion | Página sintética y bloques paginados; contar hijos esperados. | Página hermana/descendiente no autorizado; token sin Read content; no usar Insert/Update para resolverlo. Estado `truncated` o bloques desconocidos impiden afirmar lectura íntegra. |
| Drive | `files.list` con campos mínimos y `files.get`/export según MIME del fixture. | Archivo fuera de allowlist, descarga excesiva, URL firmada expirada; releer metadatos sólo si está permitido. Scope de metadatos no se trata como permiso de contenido. |
| n8n | Respuesta de listado sintético proyectada a metadatos aprobados. | Nodos o secretos incrustados no llegan al paquete. Rechazar ejecutar/activar aunque el token falso del backend pudiera hacerlo. Un test del wrapper no certifica que la key real sea read-only. |
| X | Post sintético por ID con contador de recursos y presupuesto cero. | Con presupuesto cero la ruta real no se llama. Simular saldo insuficiente y 429; no recarga. OAuth sin write, sin DM ni offline por defecto. |

## T10: `--ignore-user-config` y aislamiento del consumidor

Este ensayo se autorizaría en otro encargo. No se ejecutó `codex exec` anidado ni se abrió una sesión adicional.

1. En tests unitarios del lanzador, usar ejecutable sintético que sólo capture argv saneado y nombres de variables, sin valores. Comprobar que ejecutar y reanudar preservan `--ignore-user-config`, perfil y manifiesto por tarea, y que revisor no recibe conectores/secretos.
2. Con un `CODEX_HOME` temporal aislado y sin auth real, poner configuración global ficticia con un MCP “sentinela” que falle si arranca. Esto sólo prueba construcción/configuración local; no leer ni copiar `auth.json`.
3. Caso sin overrides: ignore debe evitar cargar el sentinela. Caso con overrides explícitos: seleccionar exclusivamente fixture stdio read-only. Capturar catálogo exacto; pedir tool de escritura por nombre y comprobar denegación antes de backend. Si requiere inferencia autenticada, dejar ese tramo pendiente hasta disponer de autorización de sesión/cuota; no usar API key para suplirlo.
4. Para paquete C, consumirlo con todas las credenciales de terceros ausentes: hash y contenido se verifican igual con ignore. La herramienta de actualización del origen no existe en ese canal. Comprobar por separado que otros conectores amplios no estén disponibles al consumidor; offline no elimina capacidades externas que el runtime ya le otorgue.
5. Ensayo final posterior, autorizado, en **un único** hijo real del harness: registrar versión CLI, modelo solicitado/observado cuando haya evidencia, argv saneado, catálogo y operación de fixture. Retomar mismo SID y mismo paquete, sin nueva exportación. Sólo entonces se podrá declarar integración real.

La documentación de configuración es más amplia y puede evolucionar respecto del binario 0.167.0. Una tabla TOML válida no prueba que se hayan aplicado allowlists, OAuth o overrides bajo ignore; este ensayo debe resolverlo. Para una credencial de proveedor estrictamente read-only, corroborar permisos en su mecanismo oficial y usar un recurso de prueba. No enviar una escritura real al recurso productivo como test negativo.
