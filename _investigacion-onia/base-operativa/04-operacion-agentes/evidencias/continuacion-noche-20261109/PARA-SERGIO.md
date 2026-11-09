# Para retomar por la mañana

El cierre técnico, pruebas, cuota y hashes se consultan en [INFORME](INFORME.md). Esta guía ordena el uso del material; no sustituye las tareas canónicas ni concede permiso de publicación.

## 1. Cerebro → ensayo del workshop → automatización

El cerebro conserva19 referentes / 79 piezas de investigación previa. La nueva consulta permite recuperar23 patrones seleccionados con fuente, hecho, límite y propuesta OnIA separados. Es una biblioteca editorial con filtros; no un modelo entrenado ni un sistema que haya visto todos los videos de forma integral. [Guía aplicada](../../../03-referentes/cerebro-operativo/20261109/GUIA-APLICADA.md).

Desde el VPS:

```bash
cd /home/onia-codex-worker/repos/onia-coordinador
C=_investigacion-onia/base-operativa/03-referentes/cerebro-operativo/20261109
python3 "$C/consultar.py" consultar --tema oferta --uso vender
python3 "$C/consultar.py" consultar --tema agenda --uso workshop --formato json
python3 "$C/consultar.py" consultar --tema contenido --uso guiones
```

El paso siguiente es ensayar los primeros 10 minutos con la guía, láminas y hoja. Tu decisión vigente dice: «Codex escribe primero solo los 10 primeros minutos; Sergio revisa; luego el resto». [Fuente](../../../05-herramientas/2026-11-08-harness/00-decisiones.md). Por eso no se declara terminado el workshop completo.

En el Chromium que ya ves en el VPS, Ctrl+O permite abrir este archivo del VPS:

```text
/home/onia-codex-worker/repos/onia-coordinador/_investigacion-onia/base-operativa/01-negocio/workshop-20261108/kit-piloto-20261109/index.html
```

El índice enlaza siete láminas, hoja de 2 páginas, guía de 3 y sus PDFs. No requiere servidor. La práctica de Claude sí requiere acceso propio e Internet. La muestra escrita no es una ejecución de Claude. Hacé el ensayo con cronómetro y completá las observaciones; si una persona no tiene acceso, esa parte queda pendiente, no se cuenta como autonomía lograda.

## 2. Fábrica de contenido: lo usable hoy

[Panel de consulta](../../../05-herramientas/fabrica-contenido/20261109-lector-panel/evidencia/panel-corregido-01/panel.html), preparado con dos guiones propios, dos guías oficiales, una noticia candidata fechada y los estados de las tareas de origen. En Chromium VPS, Ctrl+O:

```text
/home/onia-codex-worker/repos/onia-coordinador/_investigacion-onia/base-operativa/05-herramientas/fabrica-contenido/20261109-lector-panel/evidencia/panel-corregido-01/panel.html
```

G01: «Tu lista necesita tres datos». G02: «Cuando la agenda no cabe». Ambos requieren tu revisión editorial y una toma/demostración propia antes de publicar. La noticia Enterprise se excluyó de estos guiones para principiantes; no se anuncian funciones Enterprise como gratuitas.

| Parte | Alcance comprobado | Lo que falta para operarla |
|---|---|---|
| Referentes | Catálogo consultable, fuentes y límites | Selección editorial de cada nueva pieza; nuevos medios si son necesarios |
| Fuentes/noticias | Lectura manual de 3 URLs exactas y snapshot fechado | Nuevas fuentes revisadas, recurrencia aprobada y controles de actualidad |
| Ideas/guiones |2 borradores propios con fuentes | Tu revisión, demostración, grabación y permiso de publicación |
| Panel |HTML de consulta real, sin servidor | No actualiza solo ni envía aprobaciones |
| Telegram/n8n |Adaptador: 20 controles + 5 del harness; copia remota inactiva almacenada | Identificar bot/destinatario en privado, comprobar runner/webhook, autorizar prueba específica; sin mensajes reales todavía |
| Campaña |Ficha comercial y checklist | Hora/zona, canal, acceso alumnos, pago/condiciones, capacidad y soporte; después autorización para publicar |
| Video Euge |Diagnóstico y muestras del inicio | Reproducción completa o copia audiovisual autorizada; no deducir música/tono del texto |

Actualizar manualmente las fuentes crea un recibo nuevo y consulta sólo páginas públicas. No reemplaza una revisión editorial. Comando documentado, no ejecutado automáticamente por esta guía:

```bash
D=_investigacion-onia/base-operativa/05-herramientas/fabrica-contenido/20261109-lector-panel
PYTHONDONTWRITEBYTECODE=1 python3 "$D/lector.py" --salida "$D/evidencia/lectura-real-03"
```

Elegir otra carpeta nueva si ya existe. Publicar el nuevo recibo mediante el mismo proceso de entrega/revisión; no editar un snapshot para simular una lectura.

## 3. Cómo se trabajó y cómo continuar

Se abrieron 3 tareas independientes del harness: cerebro, kit y panel. Cada ejecutora tuvo una rama, un worktree y una ruta exclusiva. Las correcciones retomaron el mismo SID. Cuando una terminó, una revisora distinta ocupó un cupo. Ejecución Sol 6.1 high y revisión Sol 6.1 ultra, sin hijos en este lote. El coordinador conserva el JSON, verifica commit remoto, recoge veredicto, acepta e integra a master.

El límite de 3 es global del harness en este VPS, incluidos revisores; no se multiplica por coordinadora. La medición del lote no autoriza subirlo. Los procesos CLI no aparecen automáticamente como chats de la app. Estado desde el checkout coordinador:

```bash
python3 _investigacion-onia/base-operativa/05-herramientas/scripts/harness.py estado
```

La siguiente tarea debe tener un resultado concreto, entradas, carpeta exclusiva, aceptación y límites. Ejemplo: después de revisar el piloto, completar clase1 con tus correcciones; por separado, preparar la prueba Telegram con identidad y destinatario definidos. Si falta una dependencia real, se registra en_espera con causa y condición de retoma. Un fallo técnico se corrige en la tarea y SID existentes, no se abre una tarea duplicada para ocultarlo. Aceptación exige revisión distinta y commit remoto.

El piloto mínimo de cola ya tiene tu sí acotado, pero el scheduler aún no está implementado. Este lote lo coordinó una sesión activa; no queda un servicio permanente ejecutando tareas mientras el chat está cerrado. Platform permanece fuera. No se abren nuevas áreas sin su encargo.
