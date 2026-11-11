# Encargo fabrica-automatizaciones-meta-canales-20261111

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Preparar adaptadores verificables para comentarios/DM de Instagram y Facebook y conectarlos mediante contrato al panel existente.

## Entregable

Código, fixtures, pruebas reproducibles, contrato exportable y guía exacta de activación pendiente.

## Criterio de aceptación

Cada canal tiene recorrido local y fallos probados; diferencia estricta entre simulación y E2E real; ninguna activación/envío/gasto.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Lote técnico autorizado en CIERRE-VENTA-20261111.md (aeb1160), regla52fb1c8. Leer decisiones y bitácora; no retomar nombres/precios/horas históricas. Usar desarrollar-y-verificar. Un worktree, cero hijos, Sol high. No editar panel/harness/otros productos.
- Revisar antes implementaciones n8n y diseños de canales ya presentes en repo. Reutilizar sin activar. Única ruta nueva 05-herramientas/fabrica-onia/3-automatizaciones/meta-canales-20261111. No copiar secretos, contactos, QR o direcciones privadas.
- Investigar documentación primaria vigente de Meta para comentarios y mensajes privados IG/FB, distinguir capacidades/permisos/cuentas/versiones y fechas. Si fuente no accesible marcar desconocido; no inventar ventanas, tokens ni aprobaciones. Crear matriz canal/capacidad/entrada/salida/prueba/pendiente.
- Implementar procesamiento puro con idempotencia y estado persistente de ensayo: detectar NEGOCIO, ofrecer información vigente, conservar contexto de origen y baja, enrutar a WhatsApp sólo mediante destino privado configurado; no presumir acceso API real. Firma de webhook/verificación y límites de payload; rechazo de identidad inválida, duplicados, orden tardío, inyección, timeout/resultado incierto. Sin shell libre.
- Conector real deshabilitado por defecto, configuración privada sin tokens en logs, contrato para panel incluye estado, comprobaciones, entradas faltantes y aprobación pendiente. Simular respuestas éxito/fallo en fixtures rotulados, no registrar mensajes como realmente enviados. Preparar prueba autorizable por canal y no ejecutarla con personas. Node/Python existentes sin nuevas APIs pagas.
- Entregar README/PRUEBAS/RECIBO, comandos/salidas, commit+push rama; revisión independiente por coordinadora. Publicar estado para_revision de producto no estado canónico. Nunca declarar canal listo sin prueba real autorizada.

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

Estado: [registro de trabajo](../tareas/fabrica-automatizaciones-meta-canales-20261111.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.
