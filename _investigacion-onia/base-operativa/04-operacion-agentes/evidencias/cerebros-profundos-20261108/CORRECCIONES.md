# Correcciones antes del encargo profundo

8 de noviembre de 2026. Sergio autorizó corregir y luego ejecutar los grupos de Grok; se supera el stop anterior sólo para ese alcance.

| Hallazgo | Acción comprobada / límite |
|---|---|
| VIP presentado como vigente en fichas previas | Índice corregido y nota vigente en19fichas: Bs50 aprobado; VIPBs150 propuesto. No se inventaron condiciones. |
| Concurrencia nativa sin límite explícito | Harness configura0..2hijos por ejecutor,1enesteencargo; sin nietos; revisores0; retoma hereda salvo0explícito. La prueba real del lote acredita uso efectivo, además de tests sintéticos. |
| Retoma perdía instrucciones del revisor | Se adjuntan estado/próximo paso y último veredicto íntegro. Prueba completa de revisión cambios→retoma mismoSID→corrección→otra revisión→aceptación. |
| Diez etapas llamadas once en evidencia previa | Ya registrado el conteo correcto; se conserva evidencia original. No hay etapa funcional faltante demostrada. |
| Campo de chequeo previo decía revisión pendiente | El estado aceptado y veredicto posterior prevalecen; no se manipula el digest. Nuevos cierres separan controles hechos y próximo paso. |
| Sesiones invisibles en barra lateral | Se explica CLI/PID/log/ID; no se crean chats duplicados para aparentar visibilidad. |
| Faltan acceso propio, horario, plataforma y condiciones del workshop | Dependencias comerciales/operativas explícitas. No resolver sin datos ni activar servicios. El estudio de referentes puede avanzar independientemente. |
| Faltaban fuentes de referentes y pruebas de conectores | El nuevo estudio busca cerrar cobertura de referentes. Instalar/probar conectores es un encargo separado y no se ejecuta aquí. |

Correcciones y preparación publicadas en `e286d4564127945cb007e7b3db69cf2208e6dad7`. [Preflight](preflight.json), [tests y revisión auxiliar](correcciones-y-tests.json). Suite final:129casos,128aprobados y1omisiónWindows; cero fallos. No se tocaron scripts shell ni producción. La revisión auxiliar es distinta de las revisoras de las fichas.
