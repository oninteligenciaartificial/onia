# Prueba SSH real de Boss con la llave nueva

ID `conexion-boss-codex-20261110`. Boss, 10-nov-2026 ~08:25 America/La_Paz. Commit leído: `c7e8b20` ([INSTALACION-v1](INSTALACION-v1.md)).

- **Llave:** dedicada de Boss, huella `SHA256:XaGm1eJm0VKNyGGVvrCeUJj5nifN3GL2JTw3uXCXKuY`.
- **Opciones:** `BatchMode=yes`, `StrictHostKeyChecking=yes`, `IdentitiesOnly=yes` (sólo esta llave, nunca la vieja).
- **Destino:** el conocido. No se publican el destino ni la dirección.

| Prueba | Salida (sin cambios) | Código |
|---|---|---|
| `consultar conexion-boss-codex-20261110` | `ok:true`, revisión 7, `en_espera`, briefing `f985ecc0…9e7e85`, sin intento, `viva:false` | 0 |
| `consultar conexion-boss-piloto-20261110` | `ok:true`, revisión 2, `preparado`, briefing `c93d3030…a9db0e9`, sin intento, `viva:false` | 0 |
| Comando `id` | `{"ok": false, "error": "comando_ssh_no_permitido"}` | 2 |
| Comando `bash -c 'echo hola'` | `{"ok": false, "error": "comando_ssh_no_permitido"}` | 2 |
| SFTP `ls` | Rechazado: el cliente recibe JSON en lugar del subsistema («Received message too long») | 255 |
| `ejecutar` del juguete sin permiso local (solicitud `boss-prueba-sin-permiso-01`, revisión 2) | `{"ok": false, "error": "fallo_local_verificar_sin_secretos"}`, sin efectos | 2 |

## Resultado

**Conexión de ida con la llave nueva: correcta.** Las consultas funcionan y se rechazan el shell, los comandos arbitrarios y SFTP.

Observaciones para Codex:

1. El rechazo de `ejecutar` sin permiso devuelve un error genérico (`fallo_local_verificar_sin_secretos`) en lugar de algo como `permiso_ausente`. Funciona, pero un código más claro ayuda a diagnosticar.
2. Usé el nonce `boss-prueba-sin-permiso-01` en la prueba sin permiso. Si el diario lo registró, el lanzamiento real del juguete debe usar otro nonce. Codex debe confirmar que ese intento rechazado no bloquea la tarea.

## Pendiente

- **Sergio:** ejecutar `configurar-retorno.sh` en el VPS con la URL y la clave de la rutina "Retorno Codex → Boss (webhook)".
- **Codex:** habilitar el permiso del juguete.
- **Boss:** pedir el juguete, repetir la petición y dar el acuse.
- Restringir la llave vieja después del piloto.

No modifiqué el registro ni el briefing del harness.
