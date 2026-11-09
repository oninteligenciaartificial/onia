# Evidencia de entrega

9 de noviembre de 2026 UTC. Rama asignada `codex/ws-cerebro-consultable-20261109`, base `fa9a6e6f1714cd9dccbb5cab3f7baad177938c20`. El alcance de escritura es `03-referentes/cerebro-operativo/20261109`. El commit publicado y su cotejo remoto se informan al entregar.

## Fuentes y método

Se leyeron AGENTS, ESTADO, reglas comunes, memoria Boss, ORQUESTACION, ESTRUCTURA, arquitectura y el cuerpo canónico de desarrollar-y-verificar. La directora apareció en el catálogo de skills de esta sesión y se leyó por archivo. Las entradas de investigación fueron los índices y COBERTURA de A/B/C, el cierre de retomas, pasajes de patrón y aplicación de las 19 fichas y las propuestas SINTESIS/FUENTES-Y-MATRIZ del workshop nocturno. El catálogo conserva 28 rutas con sus huellas. [Catálogo](catalogo.json)

La selección manual produjo 23 piezas y patrones. Se reservaron las 79 piezas como conteo heredado. La validación coteja la entrega de cada grupo contra su fila del cierre aceptado y conserva modalidades, dependencias y límites. La revisión semántica de las paráfrasis queda disponible a través de pasajes, líneas y fichas completas. [Cierre de origen](../../../04-operacion-agentes/evidencias/cerebros-profundos-20261108/CIERRE-RETOMAS.md)

## Pruebas ejecutadas

```bash
C=_investigacion-onia/base-operativa/03-referentes/cerebro-operativo/20261109
python3 "$C/consultar.py" validar
python3 "$C/consultar.py" etiquetas
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s "$C" -p 'test_*.py' -v
git diff --check
```

La validación pasó con 19 referentes, 23 patrones, 23 piezas seleccionadas, 79 piezas heredadas y 28 fuentes locales. La suite pasó sus 17 pruebas, invocando el CLI desde `/tmp` y usando exclusivamente biblioteca estándar. Cubre recuperación completa, una oferta con URL y aplicación concreta, prioridad A/Erik, normalización, combinación de filtros, salida determinista, Markdown con límites y misma conversación, tema desconocido, entrada inválida, fuente faltante o alterada, URL de pieza inventada, pasaje de otra pieza, límites omitidos, ruta exterior y JSON/esquema inválidos. [Resultado de integridad](evidencia/integridad.json) · [Suite tras corrección funcional](evidencia/pruebas-v2.txt) · [Suite sobre código de entrega](evidencia/pruebas-v3.txt)

| Caso aplicado | Argumentos de consulta | Cantidad | Código |
|---|---|---:|---:|
| Ordenar | `--tema agenda --uso workshop` | 4 | 0 |
| Vender | `--tema oferta --uso vender` | 5 | 0 |
| Enseñar | `--tema ensenanza --tema revision --uso enseñar` | 8 | 0 |
| Ideas | `--tema contenido --uso ideas` | 6 | 0 |
| Guiones | `--tema gancho --tema cta --uso guiones` | 4 | 0 |
| Tema fuera de selección | `--tema tributacion --uso workshop` | 0 | 0 |

Las ejecuciones de la tabla usaron `--formato json`. El recibo conserva argumentos, IDs, URLs, modalidad y dependencia de cada coincidencia. Los fallos inducidos exigieron código 2 y stdout vacío. Se preservaron las copias alteradas en `/tmp/cerebro-consultable-pruebas-*`. El fallo de fuente faltante se ensayó incluso con una consulta que normalmente quedaría vacía. [Recibo de consultas](evidencia/consultas.json)

Se comprobaron las rutas y anclas locales de los documentos de entrega. La revisión manual de la guía comprobó la suma de 120 minutos y la incompatibilidad del bloque continuo de 40 minutos antes de las 10 frente a la llamada 09:30–10:00. Los ejemplos son casos propios de preparación didáctica. Su práctica con Claude y alumnos sigue pendiente.

## Error encontrado y corrección

La primera suite dio 16 pruebas correctas y una fallida. `test_catalogo_total_trazable` exigía límites heredados no vacíos y falló en `assertTrue` sobre `cobertura_heredada_referente.limites`. La inspección localizó `faltantes` vacío en las seis entradas de B, aunque sus fichas describen limitaciones. El primer diseño del catálogo dependía de ese campo para listar los límites específicos del referente, además de la modalidad de pieza y límites comunes ya presentes.

Se conservó el campo heredado intacto y se añadió `limites_adicionales_ficha`, con cobertura audiovisual, clase completa, atribución y privado según cada ficha. El CLI los devuelve por separado en JSON y los presenta junto a los heredados en Markdown. La prueba exige al menos una de ambas listas, y la validación sigue rechazando alteraciones de los límites de COBERTURA. Tras esta corrección pasaron las 17 pruebas. El ajuste final de legibilidad del código se comprobó con la misma suite y quedó en el recibo v3.

## Límites y condición de salida

La capacidad comprobada es recuperación local determinista por etiquetas y referencias verificadas. Las URLs conservan su atribución histórica. Su disponibilidad actual y la permanencia de medios temporales quedan fuera de esta comprobación. La sesión realizó lectura documental y pruebas offline. La cobertura audiovisual, el contenido privado, las métricas y los resultados mantienen los límites heredados por ficha.

La selección de 23 piezas, las etiquetas y las aplicaciones son decisiones editoriales de esta entrega. La validación automática verifica integridad estructural y bytes. Boss y Sergio revisan interpretación, síntesis y adopción. Sigue pendiente el ensayo humano de los ejemplos y la revisión independiente de este commit por el coordinador, seguida de integración y cotejo en `origin/master`.
