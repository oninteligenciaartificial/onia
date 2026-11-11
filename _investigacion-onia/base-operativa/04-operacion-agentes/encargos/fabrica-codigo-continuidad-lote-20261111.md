# Encargo fabrica-codigo-continuidad-lote-20261111

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Implementar despachador acotado y recuperable de lotes aprobados sobre el harness existente.

## Entregable

Implementación o paquete concreto, contrato, pruebas y recibo en rutas asignadas.

## Criterio de aceptación

Cumple el plan aprobado, evidencia reproducible, límites honestos; revisión independiente requerida.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Autorización directa actual de Sergio: Ok, vamos con el plan ve desarrollando te dejo. Plan aprobado en master aeb1160, 05-herramientas/fabrica-onia/CIERRE-VENTA-20261111.md sección Plan completo y autorización final. Leerlo y las decisiones vigentes; instrucciones actuales prevalecen sobre STOP histórico dentro del lote técnico.
- Una tarea, rutas asignadas, cero hijos. No modificar registro canónico ni instalación activa. Sin servicios, gastos, publicaciones comerciales, mensajes, n8n ni cambios de PC desde esta ejecutora. Commit y push de tu rama al terminar; coordinadora revisa e integra. No declarar terminado por un archivo escrito; comandos/salidas y límites en recibo. No secretos/IPs/QR/medios privados en Git. Modelo solicitado Sol high; observado desconocido si no hay evidencia.
- Reutilizar trabajo.py, harness_sesiones.py y diseño ESCALADO-CARRILES-PROPUESTA.md. No reconstruir harness, ni editar otros scripts compartidos; módulo nuevo invocable por coordinadora con API existente. Ver flujo diario revisado 9a4639f en rama codex/ws-fabrica-automatizaciones-flujo-diario-20261111 como referencia, sin copiar sus estados.
- Manifiesto de lote aprobado con IDs existentes, dependencias, rutas, operaciones autorizadas, vigencia y presupuesto/proveedor; autoridad de estados sólo registro canónico. Tick finito: consultar, lanzar, cerrar ejecutor, lanzar revisor, recoger, comprobar exacto commit, preparar integración. Integración/despliegue sólo con permiso explícito del manifiesto y validación; si no puedes ofrecer integración segura, exponer acción a coordinadora y límite, no fingir autonomía completa.
- Persistencia privada, lock, revisión esperada, journal intención/efecto, reconciliación por SID/commit ante fallo, no doble despacho ni IDs nuevos para eludir. Máximo3 incluyendo revisores, cero hijos, revisión prioritaria. No6altas/día ni90%. Cuota incluida disponible y proveedor comprobado; noAPI paga. Reintentos sin progreso se bloquean por tarea y continúa independiente. STOP/revocación y recuperación seguros, sin borrar evidencia ni matar procesos ajenos.
- Probar con dobles caída antes/después de despacho, ejecutor terminado sin cierre, revisor terminado, duplicados, revisión obsoleta, conflicto de rutas, falta de cuota/proveedor, reinicio y revocación. Entregar CLI documentado y ensayo real acotado preparado para coordinadora; no lanzar modelos desde tu sesión ni instalar scheduler. Entregar configuración deshabilitada y criterios para activar.

## Contexto mínimo

Leer sólo las fuentes enlazadas necesarias; rutas relativas a este briefing.

- [04-operacion-agentes/reglas-comunes.md](../reglas-comunes.md)
- [00-MAPA/ESTADO.md](../../00-MAPA/ESTADO.md)
- [04-operacion-agentes/ORQUESTACION.md](../ORQUESTACION.md)
- [06-plataforma/arquitectura.md](../../06-plataforma/arquitectura.md)
- [05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md](../../05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md)

## Skills de apoyo disponibles

No cargarlas automáticamente. Usar sólo la pertinente para una parte delimitada del encargo; no reemplazan la skill directora elegida.

- [tercero-matt-research](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md)
- [tercero-matt-writing-agents](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/productivity/writing-for-agents/SKILL.md)
- [tercero-matt-handoff-onia](../../05-herramientas/compartibles/terceros/generales/matt-pocock/handoff-onia/SKILL.md)
- [tercero-addy-context](../../05-herramientas/compartibles/terceros/generales/addy-osmani/skills/context-engineering/SKILL.md)
- [tercero-superpowers-debug](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/systematic-debugging/SKILL.md)
- [tercero-superpowers-verify](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/verification-before-completion/SKILL.md)

## Salidas de referencia del área

- Cambio acotado de código
- Comprobación del comportamiento solicitado

## Registro

Estado: [registro de trabajo](../tareas/fabrica-codigo-continuidad-lote-20261111.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.
