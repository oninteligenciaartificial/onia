# Cerebro + panel usable para Sergio · plan pendiente del sí

9 noviembre 2026 · America/La_Paz. Prioridad hasta el 14-nov: kit, ensayo y materiales que ayuden a vender el workshop. Se presenta este alcance; **no se implementa ni se lanzan ejecutoras antes del sí de Sergio**. No autoriza publicación social, envíos, producción, n8n real, compras, borrar ni relajar sandbox. Git privado conserva la documentación autorizada; una entrega técnica no aprueba una campaña.

## Qué existe y qué se reutiliza

- [Cerebro aceptado](../../../03-referentes/cerebro-operativo/20261109/README.md): 19 referentes, 23 patrones/piezas seleccionadas de 79 piezas previas; consulta offline por tema/uso, fuentes y límites. Commit de entrega `61551b82716645d59731e0e8cd330ce7531f3fd7`.
- [PANEL-DIARIO](../../../02-contenido/PANEL-DIARIO.md): portada y destinos Notion existentes; es antecedente funcional, no prueba de que cada vista/automatización esté operativa hoy. No crear otro Notion ni actualizarlo en este alcance.
- [Lector/panel aceptado](../../../05-herramientas/fabrica-contenido/20261109-lector-panel/README.md): HTML, tres fuentes exactas, dos guiones propios, estados canónicos y comprobaciones móvil/escritorio. Commit `ecb18ed45c671ea2816d653d3876620df3fb2589`. Sus README de entrega conservan frases anteriores a la aceptación; el [cierre canónico](../continuacion-noche-20261109/INFORME.md) acredita la integración.
- [Kit existente](../../../01-negocio/workshop-20261108/kit-piloto-20261109/LEEME.md): primeros diez minutos. Se enlaza para el ensayo; no se rehace ni se da por completo el workshop.

## Alcance y uso en tres pasos

Una entrada privada, legible y reproducible en el navegador del VPS que Sergio ya maneja:

1. **Elegir para qué:** vender el workshop, preparar una clase o preparar contenido. Mostrar temas del catálogo existente y los resultados correspondientes; conservar el caso sin resultados.
2. **Consultar el cerebro:** cada resultado separa hecho del referente, propuesta OnIA, pieza fuente y limitación. Enlazar el material aceptado, sin nueva investigación ni afirmar que el catálogo razona como un LLM.
3. **Trabajar la pieza:** abrir una idea/guion, ver texto completo, fuentes, estado editorial, qué falta y próximo paso. Partir de I01/I02 y G01/G02 existentes, con acceso al kit de ensayo. No simular noticias frescas, aprobaciones o publicaciones.

Será una proyección de consulta de las fuentes versionadas; no una nueva base editable ni un generador automático. Una única ruta de entrada abre en el visor privado existente, sin sitio público ni servidor de producción. El acceso no depende de terminar HOMELAB. La creación de ideas/guiones nuevos o cambios editoriales seguirá pasando por encargos y aprobación de Sergio.

## Archivos y límites de escritura

Todos bajo `_investigacion-onia/base-operativa/`:

| Archivo o carpeta | Cambio previsto |
| --- | --- |
| `05-herramientas/fabrica-contenido/20261109-lector-panel/panel.py` | Extender el render existente con navegación por objetivo/tema, cerebro y próximo paso; no crear otro panel desde cero. |
| Mismo directorio: `lector.py`, sólo si hace falta | Adaptar la proyección validada para consumir el catálogo mediante `consultar.py`; conservar validación de tareas, estados, fuentes y fechas. No ampliar catálogo web ni hacer ingesta recurrente. |
| Mismo directorio: `pruebas.py`, `visual.cjs`, `README.md` | Casos de uso/ausencias/integridad y apertura exacta; nueva evidencia en una carpeta distinta, sin sobrescribir capturas o snapshots aceptados. |
| `03-referentes/cerebro-operativo/20261109/README.md` | Guía en tres pasos y enlace a la entrada. Reusar `consultar.py`; catálogo y fichas permanecen como fuentes aceptadas. |
| `02-contenido/PANEL-DIARIO.md` | Nota vigente de alcance y entrada privada; mantener destinos e historia, señalar que datos/sesiones/orquestación/Platform quedan fuera. |
| `04-operacion-agentes/{tareas,encargos,evidencias}/cerebro-panel-usable-20261109*` | Registro canónico, recibos por rol/intento y veredicto independiente ligado al commit. |

## Aceptación verificable

- Sergio recibe una ruta de entrada concreta y puede abrirla en su visor; la prueba técnica registra apertura real y la validación humana queda separada hasta su confirmación.
- En escritorio y 390px móvil se encuentran cerebro, ideas, guiones, fuentes, estado, faltantes y próximo paso sin recortes que impidan usarlo.
- Tres recorridos reproducibles: oferta/workshop, clase/enseñanza y contenido/guion. No inventar equivalencias si una etiqueta no existe; usar el vocabulario actual.
- Los dos guiones mantienen sus bytes/fuentes y la separación entre revisión técnica y permiso editorial. Los estados se leen del registro único. Fuente faltante/alterada, catálogo vacío, filtro sin coincidencias y dato antiguo quedan visibles; nunca se convierten en aprobado/publicado.
- Pasan las suites existentes (17 cerebro y 22 panel en el recibo aceptado) más regresiones necesarias del comportamiento nuevo y prueba visual con sandbox activo. No escribir pruebas que sólo repitan el código.
- Revisora distinta, sobre el commit de entrega, con veredicto bueno antes de aceptar. El ensayo/confirmación de Sergio y cualquier publicación siguen siendo pasos propios.

## Modelos, cuota y parada

| Rol | Modelo y esfuerzo | Alcance |
| --- | --- | --- |
| Diseño e implementación | Sol 6.1 (`gpt-6.1-sol`), **high** | Un ejecutor, archivos de código delimitados. |
| Documentación y pruebas acotadas | Sol 6.1, **low** | Como máximo un hijo de la ejecutora si se necesita; archivos exclusivos, sin tocar el código del otro escritor. |
| Aceptación final | Sol 6.1, **ultra** | Sesión distinta de sólo lectura, tras el cierre publicado; ultra sólo aquí. |

Máximo tres cupos globales incluidos revisores, sin scheduler nuevo. Modelo del coordinador observado en este chat: `gpt-6-astra`, esfuerzo `xhigh`; no atribuirle el perfil low de una ejecutora futura. El reparto anterior se aplica a las sesiones que se lancen después del sí.

**Tope propuesto: 2 puntos porcentuales de cuota compartida para todo este lote**, incluyendo coordinación, ejecución, pruebas, revisión y retrabajo. Referencia observada: 65% usado el 9-nov a las 13:37:56 de Bolivia (17:37:56Z), saldo extra 0. Tomar una lectura nueva `U0` antes del primer lanzamiento; no fijar el techo con una lectura vieja. Reservar un punto para revisión/corrección: al llegar a `U0+1`, detener ampliaciones y evaluar si hay una entrega revisable; al llegar a `U0+2`, no iniciar más llamadas y dejar checkpoint/en_espera. Si no hay lectura fresca o margen para terminar una etapa, parar antes. El contador es redondeado/compartido y las llamadas en vuelo pueden cruzar un umbral: es un guard operativo, no garantía de facturación. Uso ajeno también reduce el margen; no atribuir todo el delta a esta tarea. No calcular USD.

## Recibos obligatorios y faltantes

Cada recibo cerrado de ejecutor y revisor contendrá: **id, rol/sesión, modelo + esfuerzo solicitados y observados, used_percent al inicio y al final con hora/zona, intentos, resultado (`aceptada`, `rechazada` o `fallida`), commits y retrabajo** (sí/no, causa e intentos vinculados). El coordinador incorpora el commit publicado al recibo posterior para evitar un hash autorreferencial. Un borrador o espera no es un recibo final; si faltan lecturas reales se marca el hueco y no se inventan valores ni se da por cumplido ese criterio. El dictamen técnico y la aceptación canónica se distinguen.

Falta: este sí para implementar; abrir/validar la nueva entrada; revisión final; ensayo humano del kit; completar decisiones del workshop (hora, canal, acceso, pago/condiciones, capacidad/soporte); grabaciones y aprobación editorial. Telegram real, noticias recurrentes, n8n real, datos, mejores sesiones, coordinación, orquestación, medición de capacidad y HOMELAB etapa 1 requieren un **nuevo sí posterior** al cerebro+panel. Homelab ahora sólo conexión, usuario aislado y continuidad WSL; no bloquea esta entrega.

**Estado: plan presentado, esperando tu sí.**
