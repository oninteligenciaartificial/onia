# Evidencia de cierre operativo · 10 noviembre, noche de La Paz

Foto de comprobaciones, no otro registro canónico. Los estados se consultan por el puente/harness. Encargo: resolver coordinación para continuar con Boss, preservando el presupuesto del ensayo y los permisos sensibles.

| Requisito | Resultado comprobado | Pendiente / responsable |
|---|---|---|
| Retirar seis altas | Release0efe1d5 instalada; conserva auditoría. Pruebas de ocho altas sin lanzamiento | Cerrado en ese alcance |
| Publicar y leer reglas | Reglas88b5100 en master; Boss publicó acuse46a8398 de lectura y configuración declarada de sus rutinas | No se inspeccionó directamente su app; los casos operativos se prueban por evidencia |
| Recoger revisiones terminadas | Chatbot y guionesv1 r14→r15 por `recoger`, dictamen cambios en ambos; publicados d4e8bb9/c55773d. Repetición de la misma solicitud: repetida=true, sin nuevas sesiones | Correcciones comerciales/aceptación aparte; guionesv1 sustituido porv2 |
| Consultar coordinación desde Boss | Añadidos sólo lectura de conexion-boss-codex-20261110 y homelab-conexion-20261109; consultas reales correctas | No se dieron nuevos permisos de lanzamiento |
| Comunicar sin copiar prompts | Pedido de coordinación enviado una vez por webhook; Boss lo derivó al chat principal y publicó acuse. Identifica correctamente que no era fin de sesión | Correcciones al acuse enviadas como evento distinto y acusev2 solicitado |
| Aviso real de dictamen | `notificar` de chatbotr15: HTTP recibido; repetición idempotente; se conservan dos sesiones, para_revision, sin aceptación | Falta observar el procesamiento de ese aviso específico por Boss |
| Política de cuota | Ajuste revisado e instalado enffa10a0;74 pruebas +1 caso adicional +6 sobre runtime; todos correctos. Default90 intacto | Sergio decide reserva ordinaria; consulta pendiente. El ensayo91→93 no se reabre |
| Homelab | TailscaleRunning, PC de casaOnline; puerto dedicado2224 sin banner en10s. No hubo autenticación ni cambios enPC desde Codex | Boss comprueba acceso de su app y retoma revisada; después Codex verifica huella/aislamiento |
| Concurrencia mayor de3 | No se lanzó nuevo ensayo ni se midió cinco; variante anterior revocada | Mantener3. Ensayo separado pendiente de condiciones/presupuesto |

El acuse de Bossv1 requiere corregir la confusión registro/lanzamiento y cotejar el sí previo del alta antes de pedirlo otra vez. La consulta local al socket de Tailscale falló dentro del sandbox; la misma lectura autorizada fuera del sandbox confirmó Running/Online. No se reinició Tailscale por confundir ese rechazo con daemon caído.

La fecha20:05 del acuse es declarada por Boss; los recibos HTTP conservan sus fechasUTC. No se atribuye consumo de cuota a una sesión particular. Los cambios de configuración de lectura tienen respaldo privado; la instalación posterior conservó esa configuración. No se modificó n8n, producción, secretos ni la laptop.

Este informe no declara el conjunto cerrado. Cada fila pendiente conserva su responsable; no se marca evidencia ausente como prueba pasada.
