# Preparación v4 lista; homelab pendiente

Producto revisado: `86bd35f99fd9cc7e7f53fa7f00e747cbcced3fcc`. Instalador SHA256 `0f6ca971dd570d8e783061ee1f4f58c7517f165dbf2fdb3452a9dc4140282cc1`.

La coordinadora reprodujo las 33 pruebas con Bubblewrap real en el VPS, sin omisiones; recibo y salida en `evidencia-v4-host/`. No se ejecutó el instalador administrativo en el VPS ni en la PC.

[Primera revisión](REVISION-v4-2-20261111.json): cambios por faltar alta real, SSH, inventario y persistencia. [Revisión complementaria](REVISION-v4-3-20261111.json), sobre el MISMO commit: instalador y comando listos para un intento local supervisado, sin defectos bloqueantes detectados; 19 pruebas repetidas por el revisor. Conserva el veredicto global cambios. No se acepta la tarea completa ni se oculta el primer dictamen.

Se integra únicamente la preparación revisada. [Guía y comando PowerShell](RETOMA-MONTAJE-v4-20261111.md). La revisión de PowerShell es estática; su ejecución real corresponde a Sergio en DESKTOP-0GGGNMF. Mantener el respaldo original y ejecutar una sola vez. Si falla, conservar salida saneada y detenerse sin repetir.

## Próximos pasos y condición de cierre

1. Sergio: descargar el archivo publicado y verificar hash; ejecutar la retoma v4. Recoger `alta_local=OK` o diagnóstico de bloqueo. No supone aceptación remota.
2. Coordinadora con la PC conectada: validar listener dedicado, acceso Tailscale, huella confiable antes de autenticar y llave dedicada. Probar UID/grupos, permisos, aislamiento y persistencia entre conexiones. Puerto 2222 excluido; no usar la laptop.
3. Comprobar comportamiento WSL ante cierre/reinicio en una ventana acordada. No presentar systemd activo como prueba de persistencia.
4. Ensayo de orquestación: primero una tarea real acotada en el worker y coordinación en VPS; después medir concurrencia y recuperación con las rutas exclusivas del harness. El tope ordinario sigue en tres. No activar cinco por sumar CPU de dos equipos. La ampliación y el despacho distribuido de SCHEDULER.md siguen pendientes de implementación/medición; F1-PLAN.json histórico no es ejecutable ni acredita una prueba.

El registro canónico queda en espera del resultado local; no lanzar ni aceptar tareas adicionales con este cierre. Lo único listo aquí es el instalador revisado para retomar el alta.
