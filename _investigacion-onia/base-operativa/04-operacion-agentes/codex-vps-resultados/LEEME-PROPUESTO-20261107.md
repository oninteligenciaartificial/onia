# Operación manual vigente

Único ejecutor: Codex mediante ChatGPT Sol, modelo `gpt-6.1-sol`. Sin API, Claude, fallback, subagentes ni llamadas anidadas. Solo una tarea manual a la vez; ninguna activación automática.

El modelo trabaja en `read-only`. En ejecución headless, la aprobación efectiva es `never`: las solicitudes de escalación se rechazan. Esto no desactiva el sandbox ni autoriza bypass. El envoltorio exterior conserva los artefactos.

Fuente real autorizada para lectura: `/home/onia-codex-worker/repos/onia`, rama `master`, HEAD verificado `e55812ce1bc8ef798fb370257ba887d07acccc53`, checkout limpio según la comprobación aportada. No modificar ni ejecutar scripts del repositorio.

Sin red de herramientas, credenciales, privados, producción, instalaciones, publicaciones, contactos, pagos, push o deploy. No utilizar conectores heredados. Ads pausados; cobros reales desconocidos.

Lee el encargo y recupera estado mediante `registro.tsv`, `tareas/` y `resultados/`. Consulta:

- `resultados/MANUAL-SERGIO-VPS-20261107.md`
- `resultados/INVENTARIO-WORKSHOP-20261107.md`
- `resultados/CONTINUIDAD-T003-20261107.md`
- `resultados/T003-estado.json`

T002 está completada: no reactivarla. T003 terminó con rc0; T004 la acepta técnicamente como documentación. Esa revisión separada no equivale a aceptación humana/comercial. `hechas` solo indica ejecución terminada correctamente.

Siguiente prueba pendiente: reanudar T003 usando su session ID exacto, restricciones actuales, lock y timeout del manual. No se ha probado todavía. Ningún reintento automático; los fallos requieren revisión manual.

Autonomía 24 h: cero. No hay daemon, persistencia garantizada ni cuota garantizada; cuota restante desconocida.

El LEEME anterior se conserva como histórico, sin vigencia instructiva.
