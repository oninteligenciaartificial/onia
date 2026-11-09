# Kit del piloto · entrega para revisión

9 noviembre 2026 UTC. Material escrito para ensayar los primeros diez minutos; deriva del piloto `noche-20261109`, sin ampliar clases ni cambiar decisiones. **Versión corregida y comprobada en el host VPS autorizado:** 21 controles de navegador OK, PDFs de 7/2/3 páginas con pies comprobados en las doce páginas y capturas reales inspeccionadas por la ejecutora. La revisión independiente y el ensayo humano siguen pendientes. Chromium no se volvió a ejecutar dentro del sandbox de esta sesión.

Abrí [index.html](index.html) directamente en un navegador, sin servidor ni red. Conservá juntos los HTML, `kit.css`, `kit.js` y `evidencia/`. Las láminas también se leen por desplazamiento; hoja y guía conservan el texto sin JavaScript. La práctica en vivo con Claude requiere conexión y acceso propio, todavía pendientes.

| Archivo | Uso exacto |
|---|---|
| [laminas.html](laminas.html) | Mostrar siete láminas; botones ←/→ o teclas izquierda/derecha, PageUp/PageDown. Desplazamiento y enlaces `#s1`…`#s7` también disponibles. |
| [hoja.html](hoja.html) | Dos páginas A4 diseñadas para el participante. Seleccionar A/B y copiar con Ctrl+C/⌘C o Copiar en móvil; pegar en el chat propio. Los botones seleccionan, no afirman haber copiado. |
| [guia.html](guia.html) | Tres páginas A4 diseñadas: preparación/tiempos, prompts/referencia, observación/fallos. Leer antes del cronómetro. |
| [Recibo visual del host](evidencia/host-02/recibo-visual.html) | Capturas reales de índice, siete láminas, dos hojas y tres guías. |

Para imprimir o guardar PDF: abrir hoja/guía → Imprimir / PDF (o Ctrl+P/⌘P) → A4 vertical, escala 100 %, sin encabezados/pies del navegador. Láminas: A4 horizontal. El CSS define saltos por sección y texto completo de los prompts en impresión, separado del cuadro copiable. Paginación comprobada por Chromium en el host: [7 láminas PDF](evidencia/host-02/laminas.pdf), [2 hojas PDF](evidencia/host-02/hoja.pdf), [3 guías PDF](evidencia/host-02/guia.pdf). Revisar la vista previa al imprimir en otro navegador; no se probó una impresora física. No se instalaron dependencias.

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

## Comprobación y procedencia

- [Recibo del host](evidencia/host-02/recibo-host.json): `rc=0`, Chromium 157.0.8103.15, sandbox activado, perfil sintético propio y copia aislada. Los hashes de los ocho archivos finales y la fuente del piloto coinciden con [solicitud-host-v2.json](evidencia/solicitud-host-v2.json) y con este worktree. El coordinador ejecutó la prueba en el host; esta ejecutora recibió los artefactos permitidos y los inspeccionó.
- [Comprobación de navegador](evidencia/host-02/comprobacion.json): 21 controles OK; lectura offline, navegación por botón/teclado, selección completa de A, A/B exactos, dos rechazos materiales, ausencia de desbordes horizontales a 1280/390 px, páginas medidas en modo impresión sin exceso vertical, PDFs 7/2/3, lectura sin JavaScript y cero errores JS/solicitudes externas observados.
- [Pies por página del PDF](evidencia/host-02/pdf-paginas-ejecutora.json): ejecución local del parser stdlib sobre los PDF recibidos, doce páginas con pie propio y sin pies ajenos. [Control del host](evidencia/host-02/pdf-paginas-host.json) también rc0. Es un parser acotado a estos PDF de Chromium con ToUnicode/Flate; no rasteriza ni comprueba coordenadas generales.
- [Inspección de impresión](evidencia/host-02/INSPECCION-EJECUTORA.md): `view_image` sobre las siete láminas en emulación print y el recibo conjunto; tablas y pies de 2/3 completos. Las otras seis capturas (índice, dos hojas, tres guías) son idénticas byte a byte a las ya inspeccionadas de host-01. No hay captura móvil ni rasterización visual de PDF. Se conserva la limitación de encuadre del índice por la barra fija, documentada en la inspección anterior.
- [texto-v3.json](evidencia/texto-v3.json): comprobación documental de esta entrega: prompts, agenda/ficha, aritmética, intervalos, enlaces locales y contraste numérico. Los recibos v1/v2 quedan como historial.

**Corrección C4 de la revisión independiente:** el [veredicto sobre b832bc4](evidencia/revision-c4-b832bc4.json) detectó que el pie 2/7 pasaba a la página 3 aunque el total era siete. El [control negativo sobre el original](evidencia/rechazo-c4-host-01.json) lo rechaza en página 2 por pie propio ausente. Se redujeron sólo tipografía/padding de tablas al imprimir (`16pt`, `4px 8px`) y el comprobador ahora captura/mide también las láminas en modo print. La nueva corrida host-02 valida el ajuste; no cambia contenido ni prompts. El anterior [PDF host-01](evidencia/host-01/laminas.pdf) y su [inspección](evidencia/host-01/INSPECCION-EJECUTORA.md) se conservan: aquella comprobación contó páginas y no detectó C4.

Correcciones aplicadas del feedback: grillas a una columna y ajuste de texto a ≤600 px; antes de PDF, recarga del documento, emulación print, desplazamiento al inicio y espera de fuentes; celdas y pies impresos más compactos para evitar el exceso de 12 px en guía 3. No se quitó contenido ni se bajaron las expectativas de 7/2/3 páginas. Los ocho archivos de la solicitud v2 permanecen estables desde que se congelaron.

Repetición documental desde esta carpeta, usando un destino nuevo:

```sh
python3 comprobar-texto.py evidencia/texto-v4.json
node --check kit.js
node --check comprobar.cjs
```

Para repetir la prueba de navegador, el coordinador utiliza una copia aislada en el host autorizado con los archivos de la solicitud y `../noche-20261109/CLASE1-PRIMEROS10MIN.md`:

```sh
node comprobar.cjs evidencia/host-03
python3 comprobar-pdf.py evidencia/host-03
```

El comando de Chromium se ejecuta sólo en el host autorizado, nunca dentro del sandbox actual ni desactivando aislamiento. El comprobador Python de PDF sí se puede ejecutar aquí, sin red ni dependencias. Ambos comandos deben pasar para validar otra corrida. Guardar otra corrida, inspeccionar sus imágenes y comparar hashes antes de atribuir el resultado a una versión nueva.

Historial conservado sin sobrescribir: [fallo original bwrap](evidencia/comprobacion.json), [diagrama original](evidencia/recibo-visual.html), [primera inspección](evidencia/INSPECCION.md) y [manifiesto v1](evidencia/manifiesto-v1.json). El diagrama anterior no es captura y su estado describe la entrega inicial. No se cambiaron AppArmor, bwrap, cuentas ni visor. Sólo se copiaron PNG/PDF y recibos públicos del host, nunca perfiles o cookies.

Errores registrados: un volcado inicial de fuentes se truncó y se releyó; Chromium falló dentro del sandbox; la prueba de propuesta del coordinador detectó desborde móvil, PDF de 6 en vez de 7 páginas tras capturar y exceso vertical en guía 3. Se aplicaron los ajustes acotados, luego se congelaron los archivos y se obtuvo una corrida nueva sobre sus hashes. La prueba previa de propuesta no se presenta como prueba final. Los dos fallos materiales del caso (omitir pausa / acortar inventario de B) siguen rechazados.

## Pendientes que no se convierten en resultados

Sergio revisa el kit y el piloto; comprueba acceso propio suyo y de participantes; ensaya con observador, cronómetro, canal y audio. La guía deja las seis observaciones vacías. Sin acceso: usar muestra, anotar «generación propia pendiente» y repetir esa parte antes de atribuir autonomía. Locución y duración real siguen pendientes. No se ejecutó Claude ni se utilizó cuenta prestada.

Precio grupal **Bs 50 aprobado**. VIP Bs 150 / cinco cupos / llamada de 30 min sigue propuesto. Horario de clase 1, zonas, canal, pagos, soporte y capacidad por resolver; los horarios del caso no son horarios del workshop. Sin invitaciones, publicaciones, mensajes, cobros ni ampliación a clases 2/3.

La ejecutora entrega sólo su rama. El coordinador conserva JSON y briefing, ejecuta cierre con conservación de worktree, encarga revisión independiente con otro SID, recoge veredicto y decide aceptación/integración. La revisión sobre b832bc4 pidió cambios en C4. La revisión independiente del commit nuevo y su integración a `origin/master` siguen pendientes y corresponden al coordinador.

## Fuentes y lectura

Fuentes canónicas locales, sin nueva investigación web ni afirmaciones actuales sobre funciones o cuota de Claude:

- [Piloto exacto](../noche-20261109/CLASE1-PRIMEROS10MIN.md), [ficha comercial](../noche-20261109/OFERTA-Y-RECORRIDO.md), [síntesis](../noche-20261109/SINTESIS-PROPUESTA.md), [controles](../noche-20261109/CONTROL-EDITORIAL-Y-PENDIENTES.md).
- [Decisiones](../../../05-herramientas/2026-11-08-harness/00-decisiones.md) y [plan](../../../05-herramientas/2026-11-08-harness/plan-workshop.md). Sus hashes están en el recibo documental.

Se leyó AGENTS, reglas comunes, Boss, ESTADO, ORQUESTACION y la directora canónica `preparar-oferta-y-embudo`; figuraba en el catálogo inicial y se leyó explícitamente desde su fuente. No se cargaron apoyos ni se consultaron ONIA-CENTRAL o datos privados. Esta carpeta no es un segundo registro de tareas: la autoridad sigue en el coordinador.
