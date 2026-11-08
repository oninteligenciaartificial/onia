# Estructura de la base operativa

8 de noviembre de 2026. La base vive en `_investigacion-onia/base-operativa/` y se reparte en ocho carpetas. Nada se borró: lo superado o duplicado está en `99-archivo/`. La raíz del repositorio conserva `AGENTS.md`, `README.md`, `.gitignore` y `.gitattributes`. En la raíz de la base sólo queda este `README.md` y las ocho carpetas.

Hay un solo estado vigente: [ESTADO.md](ESTADO.md). Los otros archivos llamados ESTADO son notas de una carpeta concreta.

## Carpetas

| Carpeta | Qué guarda |
|---|---|
| [00-MAPA](.) | Entrada, estado vigente, este mapa y la guía de skills por área. |
| [01-negocio](../01-negocio/) | Plan, oferta, workshop y recorrido comercial. Incluye la skill `preparar-oferta-y-embudo`. |
| [02-contenido](../02-contenido/) | Cerebro y panel diarios, formatos, reels, piloto D1 y la primera pieza. |
| [03-referentes](../03-referentes/) | Cerebros, fichas, corpus y transcripciones ASR de referentes. |
| [04-operacion-agentes](../04-operacion-agentes/) | Reglas, orquestación, sesiones, encargos, tareas y evidencias. |
| [05-herramientas](../05-herramientas/) | Scripts, cloud, skills restantes, terceros, accesos, n8n y el ASR del VPS. |
| [06-plataforma](../06-plataforma/) | Arquitectura y revisiones del producto ONIA Platform. |
| [99-archivo](../99-archivo/) | Historial, experimentos cerrados, auditorías y versiones superadas. |

## Dónde guardar trabajo nuevo

1. Si cambia lo comprobado o el siguiente paso del sistema, actualizá [ESTADO.md](ESTADO.md). No abras otro estado vigente.
2. Plan, precio, oferta, workshop o recorrido de venta: `01-negocio/`.
3. Pieza, guion, formato, panel o calendario de contenido: `02-contenido/`.
4. Ficha, cerebro o transcripción de un referente: `03-referentes/`. El ASR de referentes va en `03-referentes/asr/`.
5. Regla, encargo, tarea o evidencia de agentes: `04-operacion-agentes/`. El CLI escribe tareas en `04-operacion-agentes/tareas/`, encargos en `encargos/` y evidencia compartible en `evidencias/`.
6. Script, skill (salvo la de oferta), configuración cloud, acceso o herramienta: `05-herramientas/`.
7. Cambio de arquitectura o del producto: `06-plataforma/`.
8. Si es una copia superada, un experimento cerrado o un duplicado, movelo a `99-archivo/` con `git mv`. No lo borres.

Los registros privados siguen en `operacion/`, ignorada por Git. El contexto personal sigue en `privado/` y no se publica.
