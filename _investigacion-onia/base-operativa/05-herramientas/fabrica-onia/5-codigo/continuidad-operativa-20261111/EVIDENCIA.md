# Evidencia de entrega — 12 noviembre 2026 UTC

Encargo `onia-continuidad-operativa-20261111`, rama `codex/ws-onia-continuidad-operativa-20261111`, base `60522f59f3222674cc6c9d7f9364c022c60a3a65`. Cambios limitados a esta carpeta. Directora anunciada y leída desde su fuente canónica: desarrollar-y-verificar. Sin subagentes, revisores ni otras sesiones lanzadas por esta ejecutora. El cierre y la revisión independiente corresponden al coordinador.

| Comprobación | Resultado observado |
| --- | --- |
| Suite del adaptador, versión entregada | **13/13**; [salida completa](PRUEBAS-adaptador.txt). |
| Instalación | CLI real ejecutado dos veces contra directorio temporal: dos unidades idénticas; rechaza unidad diferente existente; lista vacía visible como `sin_lotes`, `avanzados=0`. |
| Unidades | `systemd-analyze --user verify` pasa sobre service/timer renderizados; systemd 255. No se habilitó el timer entregado. |
| Supervivencia del supervisor | Una unidad **transitoria** por ejecución de la suite, nombre exclusivo de prueba, Type=oneshot y KillMode=process: el hijo sintético termina y escribe su marcador después de salir el padre. La prueba retira su unidad; no modifica otras. No es una prueba con Codex real. |
| Ruta nativa de observaciones/recogida | Ejecutor sintético con APIs reales → commit/push contra Git temporal local → comprobar contenido esperado del artefacto → declaración reciente → cierre limitado por diff/HEAD/publicación → revisor sintético → recogida → pasada sin efecto adicional. Dos sesiones, un cierre, ninguna aceptación automática. |
| Recuperación/duplicados | Caída tras persistir el efecto, reconstruir Dispatcher y recuperar el mismo SID del journal; no crea otra sesión. También se comprueba recogida única, intenciones y sesiones existentes. |
| Lotes independientes | Orden explícito; STOP, expiración, hash alterado, manifiesto ausente, cuota agotada, tres cupos ocupados y plazo no impiden avanzar el otro lote. Una pasada tiene un tick por entrada. |
| Evidencia/seguridad | Declaración caducada no cierra; sin declaración fresca espera; lista cambiada se rechaza antes de abrir manifiesto; mensajes arbitrarios no aparecen en el log. No se copia stderr bruto. |
| Carrera en procesos canónicos | Inyección de ProcessLookupError en conciliación bloquea sólo esa pasada del lote; los otros siguen; tras desaparecer la condición, el mismo lote avanza una sola vez. |
| Regresión general, primera ejecución | 321 casos: 319 pasan, 1 error y 1 omisión Windows; [salida](REGRESION-inicial.txt). |
| Regresión general, repetición | 321 casos: 319 pasan, 1 error y 1 omisión Windows; [salida](REGRESION-final.txt). No se declara suite general limpia. |
| Casos fallidos aislados | Ambos pasan al repetir individualmente: [primer caso](CASO-repetido.txt), [segundo caso](CASO2-repetido.txt). |

Los dos errores generales comparten `harness_sesiones.process_start`, línea 96: leer `/proc/PID/stat` puede devolver `ProcessLookupError` cuando el supervisor termina entre abrir y leer. El código actual captura sólo `FileNotFoundError`. Se observó primero en `test_changes_review_reaches_resumed_executor_after_worktree_removed` y después en `test_private_git_rejects_worktree_symlink_with_same_basename`. Es una carrera del código existente, que no se modifica porque está fuera de las rutas asignadas. El adaptador conserva sus efectos mediante los journals existentes y continúa los demás lotes si esa API devuelve OSError. No interpreta esa excepción como ausencia de efecto ni autoriza duplicación. La coordinadora debe considerar este límite en revisión; su corrección en el harness requiere alcance propio, no otra tarea lanzada por esta sesión.

Comandos reproducibles en [README.md](README.md). Las salidas preservan los fallos iniciales, sin sustituirlos por las repeticiones favorables. `git diff --cached --check` se comprueba antes del commit. Se coteja que todas las rutas publicadas pertenezcan a esta carpeta y se publica sólo la rama asignada, sin force.

No se consultó cuota real: inicial/final desconocidas. Las pruebas de cuota usan respuestas sintéticas y el camino existente `cuota-codex`; no gastan cuota de sesiones Codex reales. Modelo/esfuerzo efectivos de esta sesión no expuestos como evidencia de runtime; no se inventan. No se tocaron registros/briefings canónicos del coordinador, servicios permanentes, n8n, Meta, producción, cuentas externas ni datos reales. No se usó sudo.

Instalación, activación recurrente real, cuota real y supervivencia de un supervisor Codex bajo la unidad definitiva esperan revisión e intervención técnica ya autorizada de la coordinadora sobre su lista concreta. La plantilla está preparada, validada y probada con trabajo sintético; no acredita servicio permanente activo. La guía incluye detección de timer anterior, requisito de linger, primer disparo revisado, pausa global, STOP por lote, conciliación y rollback sin borrar evidencia.
