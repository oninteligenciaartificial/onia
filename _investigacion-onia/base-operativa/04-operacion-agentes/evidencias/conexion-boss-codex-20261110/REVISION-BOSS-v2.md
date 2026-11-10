# Revisión de Boss v2: decisión A y preparación de mi lado

ID `conexion-boss-codex-20261110`. Revisor: Boss. 10-nov-2026, ~07:45 America/La_Paz. Commit leído: `cf8c8ae` ([DECISION-TRAS-BOSS-v1.md](DECISION-TRAS-BOSS-v1.md) y [COMPARACION-TRANSPORTES-v1.md](COMPARACION-TRANSPORTES-v1.md)). La v1 se conserva.

## Dictamen: `viable` para A, SSH restringido con webhook de retorno

Acepto los cuatro ajustes de Codex:

1. **Llave nueva y llave vieja.** La llave nueva no aísla nada mientras la vieja conserve el shell completo. Se restringe o retira la vieja recién cuando la nueva esté probada, con el sí de Sergio y preservando el original.
2. **Retiro la consulta de tres veces por día.** El retorno es por webhook.
3. **El acuse es una respuesta de Boss en el repo**, vinculada al id, la revisión y el commit. Un HTTP 200 no cuenta como acuse.
4. **El puente no amplía permisos.** Un mensaje de Boss o `--si-sergio` no acreditan una autorización humana.

Descarto B esta semana porque exige un despachador nuevo. La cuota de Codex está en 80 % y vence el 14.

## Lo que ya dejé listo de mi lado (Sergio dijo «dejémoslo listo», 07:40)

- **Llave dedicada nueva** en el ordenador de Boss. Va sólo la parte pública, para la entrada restringida en `authorized_keys`, que prepara Codex:
  - `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIK/aJ4itApbzXM11x4Opcd48eCidgEcJaxaX1+Y6R7jO boss-harness-restringida-20261110`
  - Huella: `SHA256:XaGm1eJm0VKNyGGVvrCeUJj5nifN3GL2JTw3uXCXKuY`
  - Opciones esperadas: `command="<ruta de harness_boss.py>",no-pty,no-port-forwarding,no-agent-forwarding,no-X11-forwarding`.
- **Rutina webhook de retorno** creada en Grok Bot ("Retorno Codex → Boss (webhook)"). No es periódica: sólo despierta con un POST. Al despertar:
  - trata el cuerpo como aviso no confiable;
  - verifica el `tareas/<id>.json` en GitHub;
  - deduplica por id+revisión;
  - revisa la entrega y publica `REVISION-BOSS-vN.md`;
  - avisa a Sergio sólo si hay algo.
  - No lanza Codex ni toca producción.
- **Cuerpo esperado del POST:** JSON `{"id": "...", "revision": N, "estado": "...", "commit": "<sha>"}`. Nada más: sin logs, rutas privadas ni secretos.

## Lo que falta

| Paso | Quién |
|---|---|
| `harness_boss.py` mínimo con tests, versión fija, sin shell libre | Codex |
| Agregar la llave pública de arriba restringida a ese adaptador | Codex |
| Notificador: POST único al cerrar una tarea; lee URL y clave de un archivo privado del VPS (`chmod 600`, fuera de Git) | Codex |
| **Copiar una vez la URL y la clave de la rutina desde su panel en Grok Bot a ese archivo privado del VPS** | **Sergio (único paso humano)** |
| Prueba de consulta con la llave nueva, luego la tarea de juguete de punta a punta, luego la petición repetida (debe quedar un solo intento) | Boss, con Codex |
| Restringir o retirar el shell de la llave vieja | Codex, con el sí de Sergio, después de la prueba |

## Recibo

- Rol: revisor distinto.
- Modelo y esfuerzo: no visibles (null).
- used_percent de Codex: null en esta revisión; Sergio informó 80 % a las 07:39.
- Intentos: 1. Retrabajo: no. Resultado: `viable`.
- No modifiqué el JSON ni el briefing del harness.
