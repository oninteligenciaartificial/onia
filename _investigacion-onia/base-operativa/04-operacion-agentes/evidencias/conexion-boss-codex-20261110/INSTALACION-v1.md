# Instalación y comprobaciones del puente v1

10 noviembre 2026, 08:16 America/La_Paz. ID `conexion-boss-codex-20261110`.

Código `69ceedb262881469fd2eedcb0447e1a025656639`; integrado y verificado en master `d919c98fdf9f8599e4faa8099ba10edd08e6cacc`. Se conservaron las nuevas publicaciones de Boss sobre fábricas. Este informe no autoriza ejecutarlas.

Instalado en el VPS, usuario `onia-codex-worker`, sin sudo ni cambios a servicios. Release fijada en `~/operacion/puente-boss/releases/69ceedb262881469fd2eedcb0447e1a025656639/`. Manifest privado coteja SHA-256 de los ocho archivos fuente. Las dos entradas shell instaladas sustituyen únicamente el marcador de release.

Se agregó una sola llave con `restrict` y comando forzado `~/operacion/puente-boss/entrada.sh` (ruta absoluta en authorized_keys). Huella comprobada: `SHA256:XaGm1eJm0VKNyGGVvrCeUJj5nifN3GL2JTw3uXCXKuY`. Las tres entradas previas se conservaron byte por byte, con respaldo privado modo 600. No se retiró ni restringió la llave anterior de Boss; falta identificarla/probar sustitución antes de hacerlo. No se reinició SSH.

Resultados:

| Prueba | Resultado |
|---|---|
| Suite Python completa | 158 ejecutadas: 157 correctas, 1 omitida por plataforma; cero fallos |
| Puente | 28 pruebas, incluidas dentro de la suite; Git temporal, Codex sintético y HTTP simulado |
| Dos plantillas shell y entradas instaladas | `bash -n` correcto |
| Consulta por entrypoint instalado | Correcta contra registro canónico, sin cambios |
| `id`, `bash`, SFTP y comando de lectura arbitraria | Cuatro rechazos locales; no se ejecutaron sus comandos |
| Lanzamiento del juguete sin permiso local | Rechazado antes de efectos; cero sesiones reales |
| SSH real desde la llave privada de Boss | Pendiente: sólo Boss tiene esa llave |
| Webhook real y acuse de Boss | Pendientes: aún no existe webhook.json |
| Tarea real, revisor distinto e integración | Pendientes del paso anterior |

Las pruebas del entrypoint son locales, no una conexión SSH real. El revisor independiente aceptó el código para el piloto; la conexión completa sigue **en_espera**, no aceptada.

Ya existe la tarea canónica `conexion-boss-piloto-20261110`, revisión 2, preparada y asignada a `boss-piloto-ejecutor`, sin sesiones. Su salida exclusiva es `evidencias/conexion-boss-piloto-20261110/producto/resultado.txt` con `ONIA PUENTE OK` más salto de línea. No se hizo dry-run sobre ese ID. Lectura habilitada; **no hay todavía permiso de lanzamiento**. Después de consulta real y configuración privada, Codex habilita ese único permiso: Sol 6.1 low, sin hijos, máximo tres intentos; revisor `boss-piloto-revisor`, diferente del ejecutor. Antes del piloto debe comprobarse cuota vigente y modelo observado en logs; una selección CLI no prueba el modelo efectivo.

## Único paso de Sergio ahora

En su terminal SSH dentro del VPS, como `onia-codex-worker`:

```sh
bash ~/operacion/puente-boss/configurar-retorno.sh
```

Pega URL y clave sola del webhook en campos ocultos. Archivo privado resultante: `~/operacion/puente-boss/webhook.json`, modo 600, fuera del repo. No se envía nada al configurar. Avisar sólo que quedó guardado; no compartir valores. La compatibilidad del header Bearer y respuesta HTTP se verificará con Boss antes de declarar éxito.

## Paso de Boss ahora

Usar su llave nueva y su destino conocido, sin publicar IP ni ruta de la llave privada:

```sh
printf '%s\n' '{"version":1,"operacion":"consultar","id":"conexion-boss-codex-20261110"}' |
  ssh -T -o BatchMode=yes -o StrictHostKeyChecking=yes -i "$LLAVE_BOSS" "$DESTINO_BOSS" onia-harness-v1
```

Publicar `PRUEBA-SSH-BOSS-v1.md` en esta carpeta con huella pública, ID/revisión devueltos, código de salida y rechazos de shell/SFTP, sin dirección de servidor ni secretos. No editar el registro/briefing. Consultar también el juguete; no intentar lanzamiento antes del permiso. El rechazo de shell debe usar esta llave nueva, no la anterior. El procedimiento de entrega y acuse está en [ADAPTADOR-v1](ADAPTADOR-v1.md).

## Retorno pendiente y reversión

El aviso se genera al cerrar desde el adaptador o con el flag local `cerrar --retorno-boss`. Publica antes de enviar; no acepta la tarea. Sin configuración conserva `pendiente_configuracion`; si un envío es incierto no lo repite automáticamente. No hay cron ni despachador.

Para un retorno pendiente de una tarea ya cerrada, el coordinador puede usar:

```sh
python3 ~/operacion/puente-boss/releases/69ceedb262881469fd2eedcb0447e1a025656639/harness.py \
  --base ~/repos/onia-coordinador/_investigacion-onia/base-operativa \
  --operacion ~/operacion notificar-boss conexion-boss-piloto-20261110
```

No ejecutar este comando antes de cerrar el juguete; no sirve para forzar un reenvío incierto. Para pausar: escribir config con `pausado:true` bajo el lock privado, conservando su versión previa; consultas permanecen, sesiones vivas no se matan. Para revocar sólo un ID: `revocado:true` en su permiso. Conservar backups/releases y modificar únicamente la entrada nueva si hay que deshabilitarla; no restaurar authorized_keys entero sobre entradas posteriores. No borrar evidencia ni reiniciar servicios.

Cuota observada 78 % usado, 08:16 La Paz, sin saldo extra. Inicio exacto no medido; no atribuir un costo inventado. Detalle y límites: [recibo](RECIBO-IMPLEMENTACION-v1.json).
