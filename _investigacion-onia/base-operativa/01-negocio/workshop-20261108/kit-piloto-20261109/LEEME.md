# Kit del piloto · entrega para revisión

9 noviembre 2026 UTC. Material escrito para ensayar los primeros diez minutos; deriva del piloto `noche-20261109`, sin ampliar clases ni cambiar decisiones. **La aceptación completa sigue pendiente: Chromium no pudo arrancar con sandbox en esta sesión.** No hay capturas del HTML ni PDFs generados y comprobados.

Abrí [index.html](index.html) directamente en un navegador, sin servidor ni red. Conservá juntos los HTML, `kit.css`, `kit.js` y `evidencia/`. Las láminas también se leen por desplazamiento; hoja y guía conservan el texto sin JavaScript. La práctica en vivo con Claude requiere conexión y acceso propio, todavía pendientes.

| Archivo | Uso exacto |
|---|---|
| [laminas.html](laminas.html) | Mostrar siete láminas; botones ←/→ o teclas izquierda/derecha, PageUp/PageDown. Desplazamiento y enlaces `#s1`…`#s7` también disponibles. |
| [hoja.html](hoja.html) | Dos páginas A4 diseñadas para el participante. Seleccionar A/B y copiar con Ctrl+C/⌘C o Copiar en móvil; pegar en el chat propio. Los botones seleccionan, no afirman haber copiado. |
| [guia.html](guia.html) | Tres páginas A4 diseñadas: preparación/tiempos, prompts/referencia, observación/fallos. Leer antes del cronómetro. |
| [Recibo visual](evidencia/recibo-visual.html) | Mapa gráfico propio del contenido y sus límites. **No es captura del navegador.** |

Para imprimir o guardar PDF: abrir hoja/guía → Imprimir / PDF (o Ctrl+P/⌘P) → A4 vertical, escala 100 %, sin encabezados/pies del navegador. Láminas: A4 horizontal. El CSS define saltos por sección y texto completo de los prompts en impresión, separado del cuadro copiable. **Revisar la vista previa: 7/2/3 páginas son el diseño, no una paginación ya comprobada.** No se instalaron dependencias.

## Correspondencia con el piloto

| Guion fuente | Lámina | Acción / hoja |
|---|---|---|
| 00:00–01:00 | 1 | Orientar: pedir → revisar → ajustar → guardar |
| 01:00–02:00 | 2 | Caso ficticio, una persona, 09:00–11:00; ficha en hoja 1 |
| 02:00–04:00 | 3 | Sergio envía A y coteja una fila; muestra escrita rotulada |
| 04:00–06:00 | 4 | Cada participante envía A y comprueba restricciones; hoja 1 |
| 06:00–08:00 | 5 | B cambia inventario de 25 a 50; sumar antes de explicar; hoja 2 |
| 08:00–09:00 | 6 | Guardar pedido, respuesta, comprobación y decisión; cerrar y reabrir |
| 09:00–10:00 | 7 | Una persona comparte comprobación/duda, hasta 20 s |

A ocupa 105 de 120 minutos y deja 15 libres. B exige 130: faltan 10; preguntar qué cambiar. No omitir pausa, recortar inventario o desplazar bloques para fabricar éxito. La lámina B invita a calcular; la clave está en hoja 2 y guía. Las muestras son escritas por ONIA, no resultados de Claude ni de alumnos. Otra ordenación válida se admite.

## Evidencia y límite material

- [texto-v1.json](evidencia/texto-v1.json): comparación de prompts completos con fuente, agenda/ficha, duraciones, intervalos, destinos locales y contraste numérico de los colores del diseño. No valida renderizado.
- [comprobacion.json](evidencia/comprobacion.json): intento real con Playwright instalado, Chromium1252, `chromiumSandbox:true`, perfil sintético propio `/tmp/onia-kit-sintetico-*` y red deshabilitada. Abortó antes de abrir páginas: `No usable sandbox!`. La etiqueta leída del proceso de ejecución fue `bwrap//&unpriv_bwrap (enforce)`; no se atribuye una causa única. También hubo error al escribir configuración de crashpad en ruta de sólo lectura. No se accedió a perfiles de cuentas.
- [recibo-visual.png](evidencia/recibo-visual.png): diagrama original del inventario, con bloqueo explícito. Su inspección no sustituye el visionado del HTML.

Se conservó el intento fallido; no se desactivó el sandbox ni se cambió AppArmor. No se inició Xvfb: el fallo ocurre antes de necesitar pantalla. Ningún navegador quedó disponible y el lanzador informó terminación de su proceso. No se tocaron servicios, cuentas o procesos ajenos.

Repetición documental (desde esta carpeta, destino nuevo para preservar evidencia):

```sh
python3 comprobar-texto.py evidencia/texto-v2.json
node --check kit.js
node --check comprobar.cjs
```

Condición de salida del bloqueo: ejecutar el siguiente comando en un entorno autorizado que permita **este Chromium con sandbox**, manteniendo perfil sintético y aislamiento. El script usa los Playwright/Chromium ya instalados en el VPS; no instala ni modifica el sistema. No usar un perfil autenticado ni desactivar sandbox.

```sh
node comprobar.cjs evidencia/corrida-v2
```

El script preparado intenta abrir el kit offline, comparar A/B, verificar selección/navegación, restricciones/fallos, desbordes, generar PDFs y capturas por página y recibo conjunto. **Esos controles de navegador no pasaron en esta sesión.** Después de una corrida exitosa se deben inspeccionar realmente sus PNG con `view_image`, registrar hallazgos sobre esa versión y revisar PDFs/paginación. Si algo falla, conservar la corrida y corregir antes de aceptar.

Errores de esta ejecutora: el primer volcado agrupado de fuentes excedió la salida; se releyeron por separado los documentos usados. Al fallar Chromium no se reutilizó una captura histórica para aparentar la comprobación solicitada. La comprobación documental incluye dos rechazos materiales: agenda sin pausa y agenda A reutilizada para B con inventario acortado.

## Pendientes que no se convierten en resultados

Sergio revisa el kit y el piloto; comprueba acceso propio suyo y de participantes; ensaya con observador, cronómetro, canal y audio. La guía deja las seis observaciones vacías. Sin acceso: usar muestra, anotar «generación propia pendiente» y repetir esa parte antes de atribuir autonomía. Locución y duración real siguen pendientes. No se ejecutó Claude ni se utilizó cuenta prestada.

Precio grupal **Bs 50 aprobado**. VIP Bs 150 / cinco cupos / llamada de 30 min sigue propuesto. Horario de clase 1, zonas, canal, pagos, soporte y capacidad por resolver; los horarios del caso no son horarios del workshop. Sin invitaciones, publicaciones, mensajes, cobros ni ampliación a clases 2/3.

La ejecutora entrega sólo su rama. El coordinador conserva JSON y briefing, ejecuta cierre con conservación de worktree, encarga revisión independiente con otro SID, recoge veredicto y decide aceptación/integración. Nada aquí acredita esa revisión ni integración a `origin/master`.

## Fuentes y lectura

Fuentes canónicas locales, sin nueva investigación web ni afirmaciones actuales sobre funciones o cuota de Claude:

- [Piloto exacto](../noche-20261109/CLASE1-PRIMEROS10MIN.md), [ficha comercial](../noche-20261109/OFERTA-Y-RECORRIDO.md), [síntesis](../noche-20261109/SINTESIS-PROPUESTA.md), [controles](../noche-20261109/CONTROL-EDITORIAL-Y-PENDIENTES.md).
- [Decisiones](../../../05-herramientas/2026-11-08-harness/00-decisiones.md) y [plan](../../../05-herramientas/2026-11-08-harness/plan-workshop.md). Sus hashes están en el recibo documental.

Se leyó AGENTS, reglas comunes, Boss, ESTADO, ORQUESTACION y la directora canónica `preparar-oferta-y-embudo`; figuraba en el catálogo inicial y se leyó explícitamente desde su fuente. No se cargaron apoyos ni se consultaron ONIA-CENTRAL o datos privados. Esta carpeta no es un segundo registro de tareas: la autoridad sigue en el coordinador.
