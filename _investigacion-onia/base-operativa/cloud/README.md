# Preparación cloud de onia

El estado operativo único está en [ESTADO.md](../ESTADO.md). Los campos del entorno y la recuperación del checkout están en [CONFIGURAR-ONIA.md](CONFIGURAR-ONIA.md). Este directorio contiene fuentes reproducibles, sin credenciales ni sesiones.

## Instalación y arranque

Desde la raíz real del repo oninteligenciaartificial/onia:

```sh
bash _investigacion-onia/base-operativa/cloud/install.sh
bash _investigacion-onia/base-operativa/cloud/start.sh
python3 _investigacion-onia/base-operativa/scripts/harness.py doctor
python3 -m unittest discover -s _investigacion-onia/base-operativa/scripts -p 'test_*.py' -v
```

El instalador enlaza las siete skills versionadas, ejecuta npm ci e instala Chromium headless shell. package.json y el lock fijan Playwright 1.64.1. El arranque ejecuta un clic y verifica el cambio de estado en una página sintética; la captura queda bajo operacion/cloud-002/ (ignorado por Git).

El fallo de scripts ausentes se reprodujo con HEAD 4de11bb. Estaban publicados desde 66674eb; el avance a f81a5b9 resolvió la ausencia y permitió instalar Chromium 156.0.8078.4. Consultar ESTADO para las verificaciones posteriores y la aceptación del entorno publicado.

## Conexión n8n

```sh
python3 _investigacion-onia/base-operativa/cloud/n8n-inventory.py
```

El helper consume N8N_API_KEY como secreto de red del entorno, hace sólo GET al host autorizado, conserva proxy/TLS, rechaza redirecciones y devuelve estado y conteos. No imprime secretos, cabeceras, nombres ni contenido de flujos. Código 2 significa clave ausente. HTTP 200 se verificó en la preparación; repetir desde tarea nueva después de guardar el setup.

## Persistencia y navegador

Guardar fuentes y entrega saneada en Git. operacion/, privado/, node_modules y capturas no se sincronizan por el repo. La VM inicial perdió artefactos al reanudarse; no depender de esa persistencia como única copia.

Playwright está comprobado en la VM cloud. La pestaña interactiva de Sergio, su control por el agente, login y persistencia de cuentas requieren prueba independiente. No incluir cookies o perfiles autenticados en el snapshot reutilizable.

Referencias: [entornos cloud](https://learn.chatgpt.com/docs/environments/cloud-environments), [Playwright](https://playwright.dev/docs/browsers), [API n8n](https://docs.n8n.io/api/).
