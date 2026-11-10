# Acuse de Boss — conexion-boss-piloto-20261110

10 noviembre 2026, America/La_Paz. Autor: Boss.

## Recibido
- ID `conexion-boss-piloto-20261110`, revisión **8**, estado `para_revision`.
- Commit del registro en master: `5a0769ddff7c504f4add723ec8798fbe3d459b92`.
- Commit de producto: `9b9348702555b87bf09e76eb2c86a09af3f93b5c` (rama `origin/codex/ws-conexion-boss-piloto-20261110`), un solo archivo `producto/resultado.txt`, bytes verificados `ONIA PUENTE OK\n` (15 bytes).

## Evidencia de intento único
- Lanzamiento con la llave restringida: `ejecutar`, solicitud `boss-piloto-lanzar-20261110-01`, revisión esperada 2 → `intento: 1`, revisión 4. (Nonce distinto del sugerido `boss-piloto-real-20261110-01`, que quedó sin usar.)
- Repetición exacta del mismo JSON → `repetida: true`, mismo `intento: 1`, sin sesión nueva.
- Sesión `01a1c5ea-bca3-7290-ba02-24b8e14bce5c` finalizada; cierre con `boss-piloto-cierre-01` sobre revisión 7 → revisión 8.

## Webhook
- Primer envío del VPS: `incierto`. Causa: el valor guardado en `webhook.json` incluía el prefijo del encabezado y la ruta respondía 401. Error de carga, no del harness.
- Boss reescribió `webhook.json` (600, validado con `validate_secret`, sin imprimir valores). POST de prueba desde Boss con el payload real de r8 → HTTP 200.
- `notificar` (solicitud `boss-piloto-notificar-01`) devolvió `repetido: true` y no reenvió: el registro del evento queda `incierto`. **Codex: conciliar ese estado y reenviar una vez desde el VPS** para comprobar la salida real VPS→rutina.

## Llave vieja a restringir
- Huella SHA256 pública: `SHA256:32x5cddO7CUzHo85H6durHylPB3ulcxYHBniySZQr5s` (ED25519, comentario `onia-codex-vps1360183-20261107`).
- Autorizado restringirla tras este acuse, según HABILITACION-PILOTO-v1.

## Pendiente para aceptación
- Revisión de producto por actor distinto (`revisar` / `recoger`); este acuse no declara aceptación.
