# Pruebas de operación manual — 7nov2026 13:05 America/Caracas

APROBADO técnicamente para lectura/análisis acotados en VPS. No operación empresarial completa ni producción E2E.

1. RunnerT003 leyó instrucciones/HEAD y fuentes reales WS-W01/02, produjo inventario/manual/continuidad como stdout persistido por envoltorio; rc0.
2. RunnerT004, sesión distinta, cotejó fuentes y aceptó técnicamente; rc0. LEEME actualizado desde texto Codex conservando histórico.
3. Reanudación por ID original y mismo lock/timeout: recordó identificador no reintroducido antes de herramientas y recuperó estado aceptado de revisión desde dos archivos; rc0.

Exactamente3llamadas CodexSolChatGPT, sin Claude/API/fallback. Tokens usados mostrados por CLI:58972/29001/61003; no equivalen a cuota restante ni precio y no discriminan cache aquí.
Lock rechazó entrada simultánea exit2 en-curso, liberado después; ocho bloques manual bash-n0 y sintaxis resume --help0. Timeout300/KILL5 configurado, vencimiento no provocado. Errores de opciones previos quedaron visibles y corregidos antes; sin reintentos silenciosos.
Fuente /home/onia-codex-worker/repos/onia HEAD e55812ce1bc8ef798fb370257ba887d07acccc53 master, limpia al cierre. Servicios systemd running iguales al control. No workers activos al cierre; ps sin resultados devuelve1 y explica exit1 del comando de comprobación final, no fallo de modelos.
Estados6hechas/0pendientes/0en-curso/0error. T003 aceptación técnica separada en resultados/T003-estado.json. Evidencias JSON PRUEBAS-CICLO-REAL-20261107.json; inventario y manual en resultados/.

Límite actual de appWindows: no SSH directo worker configurado; cuenta locked y sin authorized_keys. No se añadieron keys ni se copió privada. Se requiere autorización para públicaWindows→worker. Mientras, consola VPS admin y runuser --login onia-codex-worker. Además listado oficial app-server filtra fuentes interactivas cli/vscode por defecto, exec requiere sourceKinds; cwd y HOME importan. UI real no inspeccionada y no sincronización garantizada. CLI resume --all --include-non-interactive validado por ayuda, no abierto; retoma exec sí probada.

No probados: interfaz/interactivo Windows, permisos escritura producto, salud apps/DB, ejecución24h/PC apagada, conectores, notificaciones, push/deploy, cuotas remanentes. No ensayo humano, cobro, oferta comercial final ni acciones externas iniciadas. Siguiente trabajo permitido: ficha WS-W01 con campos pendientes y evidencia de WS-W02, no contactos/publicación.

## Acceso directo Windows habilitado y probado —7nov2026 13:09 America/Caracas
Autorización Sergio pt96u. Privada nueva generada únicamente en Windows: C:\Users\PC\.ssh\onia-codex-worker (Ed25519, sin passphrase; ACL explícita solo usuario propietario/SYSTEM/Administradores). Nunca leída ni copiada a box/VPS/chat. Pública fingerprint SHA256:DM3ZnM6B6RLjrTaaIakYMIWvUysvggEtzTCFw1v5cMI registrada en worker .ssh0700/authorized_keys0600, propietario worker. No se cambió contraseña, sshd, cuenta onia-codex ni servicios.
Windows SSH BatchMode+IdentitiesOnly+StrictHostKeyChecking=yes+hostkey Ed25519 terminó0: id onia-codex-worker, pwd /home/onia-codex-worker, repo AGENTS legible. Host público validado por acceso root previamente confiado y comparado en Windows: SHA256:QznGw4qsC2nO6gYIjMEhHG+Lv/Ul7wICuVOWNixSRm0. Prueba usó known_hosts dedicado C:\Users\PC\.ssh\onia-codex-worker.known_hosts; app puede pedir confianza separada, comparar misma huella, nunca ignorar discrepancia. No cambiado known_hosts/config global Windows.
Campos app: nombre OnIA VPS; host onia-codex-worker@187.77.16.63 (si hay usuario separado: onia-codex-worker y host187.77.16.63); puerto22; archivo identidad C:\Users\PC\.ssh\onia-codex-worker SIN .pub. Proyecto fuente VPS /home/onia-codex-worker/repos/onia; cwd de pruebas /home/onia-codex-worker/operacion. No se promete app conectada ni importación de sesiones. Native selector como worker: ~/.local/bin/codex -s read-only -a on-request -m gpt-6.1-sol resume --all --include-non-interactive . Es instrucción para operador, no ejecutada nuevamente.
Revocar: quitar únicamente línea pública identificada por huella/comentario onia-codex-worker-Windows del authorized_keys del worker; no borrar otras entradas ni tocar SSHglobal. Este anexo supera bloqueo Windows anterior.0llamadas modelos adicionales.
