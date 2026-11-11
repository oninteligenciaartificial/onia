# Acuse de Boss v2: cierre operativo (CORRECCION-ACUSE-BOSS-v1, ffa10a0)

10 nov 2026, 20:20 La Paz. Este acuse reemplaza los puntos 3 y 4 del v1 (46a8398).

| Requisito | Evidencia | Estado | Faltante y responsable |
|---|---|---|---|
| Corrección de cuota | Aceptada: registrar no depende de que la cuota esté bajo 90%; eso se controla al lanzar o al preguntar. No se registró nada nuevo. La rutina de las 20:10 sigue **pausada**, sin borrar ni reactivar | hecho | Registrar y lanzar las pruebas cuando Sergio lo pida y la cuota lo permita. Responsable: Boss |
| Alcance de la PC desde la app | La app tenía DESKTOP-0GGGNMF conectada. Comprobación de sólo lectura aprobada por Sergio a las 20:08: hostname DESKTOP-0GGGNMF, Ubuntu WSL2 en Stopped, cuenta en el corte esperado. A las 20:15 la PC quedó fuera de línea | hecho (20:08); ahora fuera de línea | — |
| Autorización | `homelab/ALTA-DETENIDA-20261110.md`: sí de Sergio a las 13:29 y «Boss reaplica con el nuevo hash». La retoma sigue en el mismo alcance. La ejecución como root la aprobó Sergio en su tarjeta local | hecho | — |
| Continuar la instalación | Hash `0521e2f4…e871` comprobado y comando exacto de la retoma. Resultado: **ALTA DETENIDA**, porque no funciona el control PE inocuo fuera del sandbox. Detalle en `homelab/ALTA-DETENIDA-v2-20261110.md` | bloqueado | Diagnóstico y corrección: Codex. Después Boss reaplica con la PC en línea |
| Puerto 2224 y huella | No hay servicio, llave ni unidad; la cuenta sigue cerrada | no probado | Depende de alta_local OK |
| Cuota | No se lanzó Codex ni se reabrió el ensayo 91→93. La política de cuota se trata con Sergio aparte | hecho | Sergio |

No se cambió el estado canónico. El homelab no está aceptado.
