# Pendiente: conectar Codex del VPS con X, n8n, Notion y Drive

Estado: pendiente de solución (no es una limitación aceptada). Pedido por Sergio el 8 de noviembre de 2026.

## Problema
Codex en el VPS (`onia-codex-worker`) no tiene conectores (MCP) configurados: `codex mcp list` está vacío. No puede entrar a X, n8n, Notion ni Drive en una sesión directa.

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
