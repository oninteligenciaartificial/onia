# Plantilla de estrategia versionada

Copiá esta estructura sólo al preparar una estrategia autorizada; no crea tarea ni presupuesto. Una estrategia = un proyecto/edición, con ID estable y versiones inmutables. Registro del harness separado.

1. **Identidad:** ID, proyecto, versión, fecha con zona, autor, versión anterior, cambio/motivo, evidencia, dependencias afectadas.
2. **Estado documental:** propuesta / borrador preparado / en revisión / cambios pedidos / aceptada para su alcance / descartada / sustituida. Separar revisión técnica, editorial, permiso comercial y ejecución. Sólo una decisión autenticada permite aprobar; no convertir validación automática en aprobación.
3. **Situación:** hechos con fuente/fecha/localizador; desconocidos como null; hipótesis con qué observación las refutaría. Identificar qué ya existe y qué se reutiliza.
4. **Comprador y problema:** quién, situación concreta, alternativa actual, evidencia directa disponible y brecha de evidencia. No inventar clientes.
5. **Resultado y oferta:** entrega demostrable, modalidad, precio/moneda, capacidad, calendario/zona, requisitos, condiciones, soporte; lo propuesto separado de lo decidido.
6. **Mensaje y piezas:** una promesa comprobable, gancho/entrega, fuentes, guion/copy/visual, CTA/destino, formatos abiertos, ensayo de voz y permisos por versión.
7. **Recorrido:** entrada → consulta → elección → pago → confirmación del dueño → acceso → entrega → soporte; responsable, idempotencia, fallo e incidencia por paso. Omitir pago sólo si la estrategia no vende y explicarlo.
8. **Acciones:** fecha de propuesta, prioridad, salida, responsable, dependencia y evidencia de finalización. Una fecha propuesta no es agenda reservada.
9. **Recursos/coste:** horas estimadas y quién dispone de ellas; coste de prueba y despliegue, autorización aplicable, herramientas/activos privados faltantes. null cuando no se conoce; sin asignar fondos de otro fin.
10. **Medición:** resultados reales con período y procedencia, escenarios matemáticos separados, denominadores, ajustes y límites de atribución. null no equivale a cero.
11. **Prueba pequeña:** muestra autorizada, hipótesis, entrada/control, resultado observable, umbral elegido para aprender, responsable y condición de parar/descartar.
12. **Revisión y siguiente decisión:** persona/rol, objeto/versión/hash, veredicto y alcance; próximo paso y quién lo resuelve. Cambio de oferta o pieza invalida sus revisiones dependientes sin borrar originales.

Ejemplo de control de versión: corregir una hora crea v2 enlazada a v1 y a la decisión de Sergio; conserva el texto anterior como sustituido, marca guiones/anuncios derivados para revisión nueva y exige un dictamen del commit exacto. El [ejemplo del contrato](CONTRATO.md#ejemplo-de-corrección) muestra esa mecánica sin emitir aprobación.
