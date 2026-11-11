# Retoma v4 autorizada por Sergio

Sergio pide: corregir el instalador, probarlo, revisión independiente, publicar en master y dar el comando para terminar el homelab y después probar orquestación. ESTA RETOMA prevalece sobre el briefing histórico: puerto2222 es ajeno y está excluido; no usarlo. No actuar sobre PC desde esta sesión ni ampliar sesiones; entregar código revisable para ejecución local de Sergio.

## Evidencia exacta

PC DESKTOP-0GGGNMF, WSL Ubuntu. Instalador v3 SHA256 3e6406591fa37c8518c42f5a4cc3e7e83885285e5836621988911b66d1e656be. Diagnóstico control_pe.ok=true rc0. Retoma --apply --resume-backup /root/onia-worker-originales-20261110T173148Z --resume-pe-control avanzó hasta CHECK vía setpriv uid/gid1001. Falló antes de bwrap: mounts_safe, DENEGADO: submontaje no aprobado. Diagnóstico acotado del usuario encontró sólo /usr/lib/modules/6.18.33.2-microsoft-standard-WSL2, tipo overlay, dentro de las fuentes. Código/árbol parcial están más avanzados que v2: no repetir el instalador anterior.

## Alcance y aceptación de esta entrega

Sólo escribir en 04-operacion-agentes/homelab. Reutilizar alta-onia-worker.py, tests y documentación. Preparar corrección estricta que mantenga ocultos módulos del kernel dentro del worker, sin permitir submontajes arbitrarios. Validar ruta/tipo/canonicalidad/descendientes y preservar rechazo de otros montajes. No debilitar controles de usuario, namespaces, seccomp, Windows, sudo, SSH, host key ni padres root. Evaluar máscara tmpfs para /usr/lib/modules (como /usr/lib/wsl) y añadir CHECK que pruebe su ocultación. No basta ignorar el error.

Retoma explícita y segura del árbol dejado por v3: verificar identidad cerrada, backup ORIGINAL, archivos esperados (bytes/metadatos), ausencia de llave/unidad/publicación antes de modificar; conservar wrapper/runtime/config anteriores mediante respaldo, no borrar. Rechazar estado distinto, archivos/enlaces/montajes extra, permisos incorrectos y ejecuciones repetidas. Tener en cuenta que ld.so.cache/localtime se copiaron del host; no asumir contenido sin validarlo. El wrapper antiguo debe autenticarse contra los bytes exactos revisados, no aceptar cualquier archivo. No sobrescribir un estado nuevo si otro paso falla. Si no se puede completar una retoma segura con evidencia disponible, entregar diagnóstico saneado mínimo del estado para Sergio, no inventar el estado.

Reproducir error con fixture del montaje observado; pruebas positivas y negativas de montaje y retoma (incluida preservación si falla). Ensayo real bwrap en VPS cuando entorno lo permita; no declarar WSL/SSH real probado con fixtures. No instalar el worker en VPS. Mejorar diagnóstico acotado de CHECK si vuelve a fallar, sin volcar secretos/entorno/stdout arbitrario.

Entregar guía v4 con un único archivo descargable, hash SHA256, comando PowerShell con comprobación de hash y retoma correspondiente, cuándo detenerse. Mantener versiones/recibos anteriores. Revisar portabilidad Windows PowerShell5.1/WSL. Documentar comandos y salidas de tests, qué no se probó, criterios para posterior SSH y orquestación. Commit y push de la rama asignada. Coordinadora repite checks, lanza revisor distinto y publica master. No integrar ni lanzar otras sesiones desde el ejecutor.
