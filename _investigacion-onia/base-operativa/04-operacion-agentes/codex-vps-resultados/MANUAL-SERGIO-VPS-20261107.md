Sergio: necesitas una **consola VPS ya autenticada como administrador**. Esta guía no configura acceso desde tu PC ni supone que su SSH funcione o que tenga la clave de esta máquina.

Entrá al usuario de trabajo:

```bash
runuser --login onia-codex-worker
cd /home/onia-codex-worker/operacion
```

Revisá antes de iniciar:

```bash
cat AGENTS.md LEEME.md
cat registro.tsv
ls tareas/pendientes tareas/en-curso tareas/hechas tareas/error
ls resultados
```

LEEME conserva afirmaciones históricas superadas: T002 ya tiene resultado; el runner actual usa `read-only`. No reactivar T002. Revisá el resumen y la salida de la ejecución elegida. No abras credenciales, `.env`, privados ni archivos internos de autenticación.

Cuando no haya trabajo activo:

```bash
./ejecutar.sh --comprobar
```

Comprueba estructura y lock sin invocar Codex. No se ejecutó dentro de T003: esta llamada ya mantiene el lock y el modelo tiene lectura solamente.

**Crear y ejecutar un encargo nuevo**

Elegí un nombre simple que no exista en ninguno de los cuatro estados. Este ejemplo evita sobrescribir el pendiente:

```bash
(
  set -o noclobber
  cat > tareas/pendientes/T004-REVISION.txt <<'EOF'
Revisar secuencialmente T003 usando su salida guardada.
Solo lectura del checkout autorizado y operacion pertinente.
Sin modelos anidados, subagentes, red de herramientas ni scripts del repo.
Sin privados, credenciales, cambios de repo ni acciones externas.
Entregar hallazgos y criterio de aceptación por stdout.
EOF
)
```

Si hubo error o el nombre ya existe, detenete; no ejecutes un archivo anterior creyendo que contiene el nuevo encargo. Tras comprobar el contenido:

```bash
cat tareas/pendientes/T004-REVISION.txt
./ejecutar.sh T004-REVISION.txt
codigo=$?
printf 'Código del runner: %s\n' "$codigo"
```

Un solo trabajo. El runner copia el prompt, registra inicio, mueve a `en-curso` y guarda `salida.txt`, `rc.txt`, `resumen.txt` en un directorio único de `resultados/`. Al finalizar registra fin y mueve a `hechas` si Codex devuelve 0; en otro caso, a `error`.

**Hecha no significa aceptada.** Revisá salida, código, fuentes y límites. Registrá fecha, revisor, resultado revisado y decisión explícita en un archivo nuevo de `resultados/`, fuera del repo. El modelo entrega texto; el envoltorio guarda archivos. Headless usa aprobación efectiva `never`: rechaza escalaciones, sin aprobación humana ni bypass.

**Reanudar el mismo contexto**

Buscá `session id:` en la salida guardada de esa ejecución, no en archivos de credenciales:

```bash
rg -n 'session id:' resultados/T003-CICLO-REAL.txt.E6P3eh/salida.txt
```

Copiá el ID exacto; no uses `--last`. La ayuda local comprobó `codex exec resume [SESSION_ID] [PROMPT]`, `--ignore-user-config` y sandbox en el comando padre `exec`. Reanudación headless por ID y archivos comprobada el7nov; visualización app e interactivo aún no probados.

Prepará un archivo nuevo `tareas/pendientes/T003-RETOMA-01.txt`, sin sobrescribir, con el paso autorizado y **todas las restricciones actuales**. Después de cerrar y revisar el trabajo anterior, este bloque usa el mismo lock, entorno y límite temporal, guardando evidencia independiente. Sustituí el ID antes de ejecutarlo:

```bash
SESSION_ID='PEGAR-ID-EXACTO'
(
  umask 077
  exec 9>>.ejecutar.lock || exit 2
  flock -n 9 || exit 2
  run=$(mktemp -d "$PWD/resultados/T003-RETOMA-01.XXXXXX") || exit 2
  cp tareas/pendientes/T003-RETOMA-01.txt "$run/prompt.txt" || exit 2
  printf '%s\tT003-RETOMA-01\tinicio\t-\t%s\n' \
    "$(date -u +%FT%TZ)" "$run" >> registro.tsv || exit 2
  timeout --signal=TERM --kill-after=5s 300s nice -n 10 \
    env -i HOME=/home/onia-codex-worker USER=onia-codex-worker PATH=/usr/bin:/bin \
    /home/onia-codex-worker/.local/bin/codex \
    -a on-request \
    -c 'model_provider="openai"' \
    -c 'sandbox_workspace_write.network_access=false' \
    exec --sandbox read-only resume \
    --ignore-user-config --model gpt-6.1-sol --skip-git-repo-check \
    "$SESSION_ID" - < "$run/prompt.txt" > "$run/salida.txt" 2>&1
  rc=$?
  printf '%s\n' "$rc" > "$run/rc.txt"
  printf 'Retoma T003; rc=%s; revisión pendiente\n' "$rc" > "$run/resumen.txt"
  printf '%s\tT003-RETOMA-01\tfin\t%s\t%s\n' \
    "$(date -u +%FT%TZ)" "$rc" "$run" >> registro.tsv
  printf 'Evidencia: %s\n' "$run"
  exit "$rc"
)
```

Es una invocación manual documentada; no modifica el runner ni mueve automáticamente estados de tareas. Registrá su revisión antes de decidir cualquier continuación.

**Parar o recuperar**

Primero `Ctrl+C` en la terminal del trabajo. Para localizar candidatos propios:

```bash
ps -u onia-codex-worker -o user=,pid=,ppid=,comm=
```

Identificá el `timeout` de tu trabajo por usuario y relación de procesos; si es ambiguo, no mates nada. Con PID inequívoco, usá `kill -TERM PID`. Nunca servicios, grupos ajenos ni terminaciones masivas.

Si queda `en-curso`, revisá procesos, lock y evidencia antes de mover o reintentar. No borres `.ejecutar.lock`: cuando no haya proceso, `--comprobar` verifica si puede adquirirlo.

Cerrar terminal o chat no garantiza persistencia. Los archivos y el session ID permiten recuperar contexto; esto no es daemon ni operación 24/7. Cuota agotada debe quedar como error visible, sin fallback/API ni reintento ciego. Efectos externos inciertos requieren conciliación antes de reintentar; aquí están prohibidos. No ejecutar scripts del repo, instalar, publicar, contactar, gastar, hacer push/deploy ni añadir otro motor.

## Pruebas cerradas y acceso desde Windows — 7nov2026,13:05 America/Caracas
Las tres llamadas autorizadas terminaron rc0: inventario desde repo real, revisión separada que aceptó técnicamente y retoma misma sesión que recordó el marcador antes de leer solo estado/revisión. Fuente Git limpia, mismo HEAD; servicios sin cambios.6hechas técnicas/documentales,0pendientes/activos/errores. No son ventas ni aceptación humana. Timeout configurado, vencimiento no provocado.

Para ver nuestras sesiones desde una terminal YA situada como worker, sin nueva llamada modelo:
```bash
cd /home/onia-codex-worker/operacion
rg -n '^session id:' resultados/T003-CICLO-REAL.txt.*/salida.txt resultados/T004-REVISION-REAL.txt.*/salida.txt resultados/T003-RETOMA-01.*/salida.txt
```
La ayuda instalada0.167.0 confirma el selector que incluye trabajos no interactivos:
```bash
/home/onia-codex-worker/.local/bin/codex -s read-only -a on-request -m gpt-6.1-sol resume --all --include-non-interactive
```
Este comando abre la interfaz; no lo ejecutamos ni enviamos un mensaje para no consumir otra invocación. No usar mientras haya runner activo. La retoma headless por ID del bloque anterior sí fue probada. Sesión T003:01a1b6f1-cda3-70d2-9a33-0e5cb67b311b.

La documentación oficial https://developers.openai.com/codex/app-server (thread/list) dice que el listado por defecto incluye solo fuentes cli/vscode; exec requiere incluir esa fuente. También permite filtro exacto cwd. Esto explica por qué un selector puede omitir nuestros jobs; no demuestra qué filtros usa tu versión de la app Windows. No se promete sincronización/importación automática ni se modifica la app. Cwd de sesiones es /home/onia-codex-worker/operacion; repo fuente /home/onia-codex-worker/repos/onia. Nombre visible de conexión no prueba usuario SSH. HOME del worker es /home/onia-codex-worker; nuestras ejecuciones no fijaron CODEX_HOME (por defecto .codex de ese home). No copiar tokens ni cambiar home0700.

Acceso SSH directo worker desde Windows NO configurado: comprobado passwd status L (sin contraseña utilizable), authorized_keys ausente, SSH22 escuchando, configuración global pubkey yes/password no. Nombre de host es187.77.16.63; puerto22 es numérico, jamás una clave pública. Archivo de identidad debe ser una PRIVADA existente en Windows; la privada root de la box no está en tu PC ni debe copiarse. No se añadió ninguna clave worker ni cambió su contraseña. Para habilitar conexión directa hace falta autorización específica para añadir al worker una pública generada legítimamente en Windows. Hasta entonces usa consola administrativa VPS ya autorizada y runuser --login onia-codex-worker (comprobado usuario/home); no alterar cuenta onia-codex vinculada al harness. No guardes el formulario incompleto ni repitas login como solución a este bloqueo.

## Acceso directo Windows habilitado y probado —7nov2026 13:09 America/Caracas
Autorización Sergio pt96u. Privada nueva generada únicamente en Windows: C:\Users\PC\.ssh\onia-codex-worker (Ed25519, sin passphrase; ACL explícita solo usuario propietario/SYSTEM/Administradores). Nunca leída ni copiada a box/VPS/chat. Pública fingerprint SHA256:DM3ZnM6B6RLjrTaaIakYMIWvUysvggEtzTCFw1v5cMI registrada en worker .ssh0700/authorized_keys0600, propietario worker. No se cambió contraseña, sshd, cuenta onia-codex ni servicios.
Windows SSH BatchMode+IdentitiesOnly+StrictHostKeyChecking=yes+hostkey Ed25519 terminó0: id onia-codex-worker, pwd /home/onia-codex-worker, repo AGENTS legible. Host público validado por acceso root previamente confiado y comparado en Windows: SHA256:QznGw4qsC2nO6gYIjMEhHG+Lv/Ul7wICuVOWNixSRm0. Prueba usó known_hosts dedicado C:\Users\PC\.ssh\onia-codex-worker.known_hosts; app puede pedir confianza separada, comparar misma huella, nunca ignorar discrepancia. No cambiado known_hosts/config global Windows.
Campos app: nombre OnIA VPS; host onia-codex-worker@187.77.16.63 (si hay usuario separado: onia-codex-worker y host187.77.16.63); puerto22; archivo identidad C:\Users\PC\.ssh\onia-codex-worker SIN .pub. Proyecto fuente VPS /home/onia-codex-worker/repos/onia; cwd de pruebas /home/onia-codex-worker/operacion. No se promete app conectada ni importación de sesiones. Native selector como worker: ~/.local/bin/codex -s read-only -a on-request -m gpt-6.1-sol resume --all --include-non-interactive . Es instrucción para operador, no ejecutada nuevamente.
Revocar: quitar únicamente línea pública identificada por huella/comentario onia-codex-worker-Windows del authorized_keys del worker; no borrar otras entradas ni tocar SSHglobal. Este anexo supera bloqueo Windows anterior.0llamadas modelos adicionales.
