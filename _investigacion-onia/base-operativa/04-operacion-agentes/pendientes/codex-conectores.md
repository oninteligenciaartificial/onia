# Pendiente: conectar Codex del VPS con X, n8n, Notion y Drive

Estado: pendiente de solución (no es una limitación aceptada). Pedido por Sergio el 8 de noviembre de 2026.

## Problema
La lista MCP global de Codex en el VPS (`onia-codex-worker`) sigue vacía. Eso no implica ausencia de plugins en una sesión: el chat coordinador respondió perfiles de GitHub/Notion/Drive y una ejecutora anunció herramientas inyectadas. No se acreditó lectura de documentos ni acceso heredado por cualquier hijo CLI, y el harness usa `--ignore-user-config`. X/n8n siguen sin acceso probado en este lote. [Análisis revisado, alternativas y pruebas pendientes](../../05-herramientas/conectores/analisis-20261108/ANALISIS.md).

## Objetivo
Que una sesión directa de Codex pueda leer y trabajar con esos servicios, sin imprimir secretos y respetando las reglas (activar n8n, publicar, cobrar o gastar solo con el sí de Sergio).

## Opciones a investigar
- Servidores MCP agregados a Codex (`codex mcp add`): n8n ya corre en el VPS; existen MCP de Notion y de Google Drive.
- APIs directas con scripts: API de n8n, API de Notion, API de Google Drive, API de X.
- Un puente desde Boss u otro agente con conectores que deje datos en archivos para Codex.

## Para cada opción, definir
Credenciales necesarias y dónde se guardan, costo, permisos mínimos, qué acciones se bloquean sin el sí de Sergio, y prueba de aceptación.

## Mientras tanto
Las tareas que necesiten esos servicios las hace Boss u otro agente con conectores.
