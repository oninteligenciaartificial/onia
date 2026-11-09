# Acceso al navegador: aprobación recibida, falta aplicación administrativa

8nov2026,20:03Caracas. Sergio autorizó continuar y dejar listo el navegador para crear personalmente la cuenta. **No falta volver a aprobar la propuesta**. El perfil exacto y los comandos siguen en [la propuesta revisada](APROBACION-APPARMOR.md).

Se intentó ejecutar el script aprobado desde el host, fuera del sandbox del agente, pero el usuario efectivo sigue siendo `onia-codex-worker`, UID1004. El script terminó rc2 en la precondición UID0, antes de crear o cargar el perfil. La escalación de herramientas no concede root. No hubo rechazo automático de aprobación.

Falta una acción de quien administra el VPS: abrir su consola administrativa, confirmar que la sesión corresponde a `srv1360183` y UID0, y ejecutar:

```bash
bash /home/onia-codex-worker/repos/onia-coordinador/_investigacion-onia/base-operativa/05-herramientas/cuentas-analisis/20261108/aplicar-apparmor-admin.sh --aprobado-por-sergio
```

No necesita compartir contraseña ni claves con Codex. Puede comunicar el mensaje final o el error sin secretos. Si no dispone de consola administrativa, la tarea permanece en espera de ese acceso; no habilitar alternativas que eliminen el sandbox.

Después se verificará el perfil cargado y el navegador con sandbox, luego autenticación/listeners/túnel, control humano en una página pública y MCP por separado. El visor permanece detenido y ninguna cuenta fue creada. No entregar la URL como operativa antes de pasar las comprobaciones. La cuenta y su nombre siguen sin confirmar en Google/Instagram.
