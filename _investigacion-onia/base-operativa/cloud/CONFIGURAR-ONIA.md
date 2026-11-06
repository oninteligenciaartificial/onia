# Aplicar el setup reutilizable de onia

Usar sólo el repo privado `oninteligenciaartificial/onia`, rama `master`. Las fuentes de este directorio deben estar subidas al repo antes de aplicar esta preparación.

En Settings → Codex Cloud → Environments → onia → Edit:

1. La ubicación elegida ahora es **Secretos de red del propio entorno onia**: `N8N_API_KEY`, dominio `n8n-sergio-n8n.hqdqgh.easypanel.host`. Sergio introduce el valor allí. No duplicarlo en la bóveda personal ni pedir o imprimir su valor.
2. Mantener el preset de registros de paquetes. Permitir `cdn.playwright.dev` y `n8n-sergio-n8n.hqdqgh.easypanel.host`. `playwright.dev` sólo es necesario para consultar documentación desde la VM. Registrar un destino de redirección bloqueado antes de ampliar la lista.
3. Aplicar el prompt siguiente al setup. Revisar resultados, guardar y **Republish/Volver a publicar**. Guardar un secreto o instalar dentro de una tarea no demuestra que una tarea nueva use esos cambios.

## Antes de ejecutar: comprobar el checkout

El error observado en «Editar onia» se debió al checkout `4de11bb`, anterior a la carpeta `cloud/`. Ambos scripts existen en GitHub desde `66674eb`. Que las doce pruebas Python pasen no comprueba la presencia del instalador ni del navegador.

En el checkout `/workspace/onia`, revisar HEAD y cambios; refrescar `master` mediante las herramientas de preparación del entorno o un avance Git fast-forward. Conservar cambios existentes y detenerse ante conflictos; no usar reset destructivo ni reconstruir archivos del historial del chat. Verificar estas rutas antes de guardar el setup:

```sh
cd /workspace/onia
git rev-parse --short HEAD
git status --short
test -f _investigacion-onia/base-operativa/cloud/install.sh
test -f _investigacion-onia/base-operativa/cloud/start.sh
```

Las rutas `cloud/install.sh` y `cloud/start.sh` por sí solas no son relativas a la raíz del repo.

## Prompt para la conversación de preparación

```text
Prepará este entorno onia usando únicamente oninteligenciaartificial/onia, master.
Comprobá HEAD y cambios; actualizá master sin descartar trabajo existente.
Verificá la existencia de _investigacion-onia/base-operativa/cloud/install.sh
y _investigacion-onia/base-operativa/cloud/start.sh antes de ejecutarlos.
Leé AGENTS.md, reglas-comunes.md y ESTADO.md. No consultar ONIA-CENTRAL.
Como instalación reproducible ejecutá desde la raíz:
bash _investigacion-onia/base-operativa/cloud/install.sh
python3 _investigacion-onia/base-operativa/scripts/test_preparar_cloud.py -v
python3 _investigacion-onia/base-operativa/scripts/test_trabajo.py -v
python3 _investigacion-onia/base-operativa/scripts/harness.py doctor
python3 _investigacion-onia/base-operativa/scripts/test_harness.py -v
Como comprobación de arranque ejecutá:
python3 _investigacion-onia/base-operativa/scripts/preparar-cloud.py --check --discovery-root /workspace
bash _investigacion-onia/base-operativa/cloud/start.sh
Verificá presencia de N8N_API_KEY sin mostrar valor ni placeholder y ejecutá:
python3 _investigacion-onia/base-operativa/cloud/n8n-inventory.py
Conservá estos comandos como Install script y comprobación de Start skill.
La habilidad de inicio debe leer cloud/INICIO-SESION.md desde la base operativa
y aplicar la skill pertinente por orquestacion.json al primer encargo, incluso
si el catálogo nativo no la anuncia. Comprobá por separado el catálogo inicial.
Guardá la configuración
mediante las capacidades oficiales de setup. Verificá red, secretos y resultado;
si falta algo, indicá el ajuste exacto sin eludir la política.
No instalar servicios en el VPS, modificar flujos n8n ni conectar otras cuentas.
Entregá resultados y configuración listos para republicar.
```

## Aceptación después de republicar

Una tarea nueva debe identificar repo, HEAD y revisión del entorno; leer esta base; comprobar los nueve enlaces en ambos niveles y la skill aplicada al encargo; pasar las suites Python vigentes y una prueba real de Playwright. Registrar aparte si las nueve skills aparecen en el catálogo nativo inicial. La API debe devolver HTTP 200 y conteos sin imprimir datos de flujos ni secretos. Exit 2 indica clave ausente; un error de red o HTTP no acredita autenticación.

Conservar resultados saneados en ESTADO.md y guardar cambios útiles en Git. Los registros privados ignorados y el estado de una VM no sustituyen persistencia compartida. No incluir sesiones/cookies de cuentas en el snapshot reutilizable.

Fuentes: [Configuración cloud](https://learn.chatgpt.com/docs/environments/cloud-environments), [navegadores Playwright](https://playwright.dev/docs/browsers).

## Inicio consolidado del 6/11

El texto preparado para el campo Start skill está en [START-SKILL.md](START-SKILL.md). Es procedimiento de arranque, no otra fuente de reglas. Guardarlo y republicar requiere verificar el resultado real; tenerlo en Git no certifica que la plataforma lo anuncie o invoque. La prueba conocida no anunció ONIA nativamente y sí permitió lectura canónica. No repetir comprobaciones de cuentas como n8n por defecto si el encargo no las necesita.
