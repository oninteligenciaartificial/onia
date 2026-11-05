# Plan inicial · histórico

Plan de arranque del 3 de noviembre, conservado desde master 14c786d. **No vigente:** consultar [PLAN oficial](../../PLAN.md). Trazabilidad, no instrucción de repetir tareas terminadas.

# Plan de puesta en marcha

Plan preparado el 3 de noviembre de 2026 para ejecutar el encargo de Sergio. [ESTADO.md](../../ESTADO.md) conserva los resultados comprobados; este plan define entregables y criterios de cierre. Las [reglas comunes](../../reglas-comunes.md) mantienen la prioridad y el alcance. El repo privado `oninteligenciaartificial/onia` ya existe y concentra estas cargas.

## 1. Corregir y comprobar el entorno cloud

Actualizar el checkout antiguo usado por «Editar onia» y ejecutar los scripts publicados de `cloud/` mediante sus rutas completas. Guardar la preparación corregida y comprobar el entorno publicado en una tarea nueva.

**Cierre:** repo y commit identificados; instalación, inicio y suites de pruebas aprobados; navegador realiza un clic con estado esperado y captura; las skills declaradas disponibles para la nueva tarea. Distinguir esta prueba Playwright de un navegador interactivo con cuentas persistentes.

La carga de n8n puede avanzar en paralelo. Su autenticación tiene una aceptación propia y no bloquea desarrollar el resto del harness.

## 2. Completar la entrada y el recorrido de encargos

Completar la entrada breve del repositorio, el mapa de áreas, el diagnóstico de archivos y la creación de briefings con registro. Reutilizar las skills vigentes y `trabajo.py`.

**Cierre:** el diagnóstico detecta un script ausente; se crea un encargo y se retoma desde otro proceso; los IDs repetidos no destruyen trabajo; un agente recibe una parte independiente y devuelve una entrega que el coordinador verifica. Conservar la entrega saneada en Git y comprobar su lectura desde Cloud.

Las rutas abarcan marketing, video, desarrollo, automatizaciones, organización y producto. Sergio pidió ahora abrir los chats cloud correspondientes, con un primer encargo concreto para cada uno. El procedimiento está en [ORQUESTACION.md](../../ORQUESTACION.md).

## 3. Usar el harness para una primera entrega comercial

Por la actualización de Sergio, después de las pruebas se prepara primero su rutina personal y el seguimiento privado en Organización. Los primeros chats de área fueron pruebas acotadas; sus ejemplos comerciales no son ofertas adoptadas. El siguiente trabajo real se encaja en esa disponibilidad.

Preparar una oferta de taller con un resultado demostrable, temario y demo. Los datos pendientes se identifican dentro de ese entregable, aprovechando lo que Sergio ya contó. Con la oferta, preparar un guion y una pieza vertical con HyperFrames.

**Cierre:** oferta revisable y demo reproducible; una pieza con imagen, texto y audio verificados; archivo final recuperable fuera de la VM. Medir cuánto trabajo manual y tiempo de producción necesita antes de aumentar la frecuencia. La venta, publicación y cobro conservan sus estados propios.

Esta entrega usa `preparar-oferta-y-embudo`, `producir-video` y, cuando haga falta construir o corregir una función, `desarrollar-y-verificar`. No espera a instalar todo el catálogo de capacidades pendientes.

## 4. Conectar y automatizar el recorrido probado

Seguir el inventario de [accesos.md](../../accesos.md) y conectar cada servicio cuando tenga una operación concreta: n8n, archivos, calendario y activos de Meta. El piloto n8n comienza con lectura autenticada; después se define el flujo que resuelve una repetición real.

**Cierre por conexión:** acceso desde el ejecutor elegido, operación mínima con resultado verificable, alcance conocido y forma de revocar. **Cierre del primer flujo:** entrada sintética, salida esperada, manejo de duplicados y fallos, y registro recuperable. Usar `automatizar-n8n` para implementarlo.

Antes de recurrencia continua se necesita comprobar disparador, límites y persistencia. La creación de ONIA Research y su inicio de sesión dependen de una superficie cloud compatible; no se consideran resueltos por instalar Playwright. Grok Bot permanece diferido y el VPS conserva la carga prevista en la arquitectura.

Cada etapa termina actualizando ESTADO.md con evidencia y próximo paso. Las correcciones se hacen en la fuente correspondiente; el plan no sustituye las pruebas ni la entrega.
