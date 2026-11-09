# Encargo noche-telegram-20261109

Área: automatizaciones
Modo: encargo
Skill directora: automatizar-n8n

## Objetivo

Preparar y probar integración mínima de fábrica de guiones con Telegram/n8n, reutilizando workflows existentes sin tocar producción

## Entregable

Adaptador determinista y workflow de prueba importable/inactivo, pruebas sintéticas, contrato con panel/harness e informe de integración real disponible

## Criterio de aceptación

1. Inventario actual saneado de Radar, Guiones, Video Intake y Command Center, distinguiendo activo/configurado/probado; sin secretos. 2. Reusar contrato y ensayo de fábrica 20261108 y registro único del harness; no otra cola canónica. 3. Entrega ejecutable y workflow n8n de prueba con entrada sintética/manual y salidas secas: nunca envío, webhook real ni LLM pago; puede preparar copia inactiva propia en n8n únicamente si creación no ejecuta nodos y se verifica active=false antes/después. No modificar workflows existentes. 4. Ruta clara panel→decisión Sergio→validación revision/idempotencia→adaptador; no afirmar panel operativo si sólo fixture. 5. Pruebas de caso bueno, dato inválido, duplicado, revisión vieja y fallo de dependencia; evidencia reproducible. 6. Documento con qué bot/credencial/destino existe, SIN valores privados ni tokens ni chat_id en Git, qué necesita autorización/prueba real y reversión que conserva originales. 7. Commit/push propios y revisor independiente antes de aceptar.

## Entrada y alcance

Un evento y resultado definido para la instancia existente de n8n.

- Encargo nocturno explícito de Sergio. Una tarea por sesión, cero hijos. Sol6.1 high por login ChatGPT incluido; no API paga, instalaciones, sudo, Docker, servicios, producción, envíos, publicaciones externas ni compras. No modificar ~/repos/onia ni leer ONIA-CENTRAL. Conservar archivos; no rm ni limpieza destructiva.
- Leer AGENTS.md, reglas-comunes, boss-memoria y 00-MAPA/ESTADO, la skill directora y sólo apoyos pertinentes. Instrucción actual prevalece sobre notas históricas. El coordinador es el único escritor de registros canónicos; no cambiar tarea/briefing/registro-de-errores. Registrar errores de esta entrega en tu carpeta para integración.
- Tiempo de trabajo objetivo 35–45 minutos; resolver el alcance mínimo comprobable. Si una dependencia externa impide, terminar la parte independiente y documentar paso exacto faltante. No perseguir alternativas indefinidamente ni inventar pruebas. Nada de cuentas, contraseñas o tokens por chat/commit.
- Hacer pruebas proporcionales y un informe breve con qué existe, qué funciona probado, qué falta, límites y siguiente acción. Guardar todas las fuentes y evidencia saneada. Git add sólo rutas propias, commit y push autónomos de tu rama codex/ws-ID; verificar ls-remote coincide. No integrar master: coordinador cierra y obtiene revisor distinto ultra.
- Leer 05-herramientas/fabrica-contenido/20261108/{DISENO.md,CONTRATO.md,ensayo.py,README.md} y skill automatizar-n8n. Consultar documentación oficial actual de n8n/Telegram para capacidades usadas, sin instalar. No inspeccionar ONIA-CENTRAL aunque un workflow lo referencie; excluirlo.
- No hay plugin n8n disponible: usar REST existente. Leer ~/operacion/reglas-n8n.txt. Credenciales en ~/.config/onia/n8n.env (0600): cargar sólo en proceso, nunca imprimir contenido, headers, URL con token ni excepciones con secretos. GET acotados; guardar evidencia sólo whitelist saneada. No exportar credenciales descifradas. Requests no siguen redirect y tienen timeout.
- IDs históricos a comprobar: NDXLJiR00ciQx72V (Guiones Diarios), QGXVyRSgrArxfolj (Radar), nAGwe7DzxNQzMxXk (Video Intake), fop5l1FEirkYoZke (demo4campos), nZkaXaZVKzgtwUqU (borradores), b6hjjNJFLuLXhRm3 (digest), vuicWsvh0hwqKhYs (Command Center, activo histórico: jamás modificar ni reemplazar webhook). Un bot admite un webhook: no usar getUpdates ni setWebhook/deleteWebhook contra bot existente. No enviar mensajes de prueba.
- Si preparás copia inactiva en n8n, nombre inequívoco ONIA · PILOTO NOCTURNO 20261109 · SIN ENVIOS, sólo nodos deterministas Manual Trigger/Code/Set, ningún Schedule/Telegram Trigger/HTTP saliente/LLM. Debe sumar a la prueba y no duplicar sin necesidad. POST sólo una vez tras buscar por nombre; si timeout reconciliar GET, jamás repetir a ciegas. Referencias Telegram/credenciales quedan en plan separado no ejecutable. No activar, ejecutar vía API ni tocar otros workflows. Si esto no es viable, JSON importable probado y causa precisa.
- Implementación mínima, sin instalar servidor/panel persistente. Se permite panel de prueba estático/interactivo aislado con datos sintéticos y esquema de comando hacia adaptador; cualquier decisión debe validar identidad/autorización en capa explícita antes de futuros eventos reales. No llamar seguro/autenticado a una maqueta. Fuentes actuales de noticias se preparan en otra sesión: acá integrar formato determinista y deduplicación, no generar contenido.
- ID noche-telegram-20261109; carpeta exclusiva 05-herramientas/fabrica-contenido/20261109-telegram; rama codex/ws-noche-telegram-20261109.

## Contexto mínimo

Leer sólo las fuentes enlazadas necesarias; rutas relativas a este briefing.

- [04-operacion-agentes/reglas-comunes.md](../reglas-comunes.md)
- [00-MAPA/ESTADO.md](../../00-MAPA/ESTADO.md)
- [04-operacion-agentes/ORQUESTACION.md](../ORQUESTACION.md)
- [05-herramientas/accesos.md](../../05-herramientas/accesos.md)
- [05-herramientas/compartibles/skills/automatizar-n8n/SKILL.md](../../05-herramientas/compartibles/skills/automatizar-n8n/SKILL.md)

## Skills de apoyo disponibles

No cargarlas automáticamente. Usar sólo la pertinente para una parte delimitada del encargo; no reemplazan la skill directora elegida.

- [tercero-matt-research](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md)
- [tercero-matt-writing-agents](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/productivity/writing-for-agents/SKILL.md)
- [tercero-matt-handoff-onia](../../05-herramientas/compartibles/terceros/generales/matt-pocock/handoff-onia/SKILL.md)
- [tercero-addy-context](../../05-herramientas/compartibles/terceros/generales/addy-osmani/skills/context-engineering/SKILL.md)
- [tercero-superpowers-debug](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/systematic-debugging/SKILL.md)
- [tercero-superpowers-verify](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/verification-before-completion/SKILL.md)

## Salidas de referencia del área

- Flujo n8n con referencias a credenciales
- Pruebas y manejo de fallos

## Registro

Estado: [registro de trabajo](../tareas/noche-telegram-20261109.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.
