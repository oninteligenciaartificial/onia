# Primer lote de análisis del repositorio

8 de noviembre de 2026 · America/Caracas. **Tres análisis ejecutados, publicados por sus propias sesiones, revisados por otras tres y aceptados.** El cierre publica sus commits originales y registros en master; el hash remoto se agrega al recibo externo después de comprobarlo.

## Qué se completó y qué sigue abierto

| Frente | Entrega comprobada | Pendientes del trabajo subyacente |
|---|---|---|
| [Workshop](../../../01-negocio/workshop-20261108/analisis-lote1/ANALISIS.md) | Recorrido completo de diez etapas, reconciliación de decisiones, ficha propuesta de piloto10min y cola con responsables/pruebas. | Hora/zona, medio de clase, acceso propio de facilitador/alumnos, condiciones de pago/entrega/soporte, ensayo y decisiones sobre propuestas. A debe preceder a B/C. |
| [Referentes](../../../03-referentes/workshop-20261108/ANALISIS.md) | Matriz de Erik/Pedro/Hormozi, fuentes públicas contrastadas y aplicación de una página, diferenciando hechos e inferencias. | Clase pública completa de Erik no estudiada; cierre privado real no observado. No se declara completado el estudio profundo de todos los referentes. |
| [Conectores](../../../05-herramientas/conectores/analisis-20261108/ANALISIS.md) | Cinco servicios, contraste chat/CLI, tres alternativas y diez casos futuros de aceptación. | Implementación, recurso de prueba y comprobación efectiva de permisos/lectura. No hay conector instalado ni prueba E2E de servicios en este lote. |

El primer paso recomendado es revisar la ficha del piloto y cerrar en un bloque las decisiones comerciales/acceso indispensables. La preparación documental comercial puede avanzar junto al piloto; no implica aprobar VIP, activar cobros, publicar o enviar mensajes. Un paquete de lectura con conexión existente es una alternativa propuesta para conectores; su prueba debe ser un encargo específico.

## Selección, autorización y alcance

Sergio autorizó revisar pendientes y elegir hasta tres para analizarlos de punta a punta. El inventario inicial tenía 15 registros: 13 aceptados y dos en espera. Uno de los dos era un control negativo que no debía ejecutarse; el otro conservaba un alcance audiovisual distinto. Los pendientes seleccionados estaban en decisiones/plan del workshop del 8/11 y en codex-conectores. [Preflight e inventario](seleccion-y-preflight.json).

Las tres tareas fueron de análisis y preparación, con carpetas exclusivas conforme a ESTRUCTURA. No se lanzaron clases B/C, automatizaciones, campañas ni el estudio profundo de 19 referentes. Ante el texto de Grokbot, Sergio confirmó analizarlo y cerrar este lote. [Evaluación del encargo](REVISION-ENCARGO-GROKBOT.md): 19 referentes implican 76–114 piezas más páginas de venta; falta precisar modelo, concurrencia de subagentes, cobertura por pieza y aceptación parcial. No se redactó la síntesis final de ese nuevo estudio, reservada a Boss.

## Cómo se midió el resultado

1. **Cobertura:** cada encargo tiene criterios explícitos para su recorrido completo, matrices, siguientes pasos y límites. Aceptar el análisis no completa automáticamente la tarea comercial/técnica investigada.
2. **Evidencia:** enlaces y cobertura por fuente; observaciones reales separadas de propuestas. Las lecturas públicas y checks locales se distinguen de ensayos humanos o contra servicios no realizados.
3. **Revisión independiente:** tres sesiones nuevas read-only cotejaron commits, criterios, fuentes y recibos. Todas dieron bueno; los seis SID son distintos. El veredicto es una evaluación contrastable, no garantía infalible.
4. **Integridad y entrega:** 70 enlaces internos nuevos comprobados sobre el árbol combinado (42/18/10), hashes de los 12 archivos originales coincidentes, diffs exclusivos y commits remotos. Los tests propuestos T01–T10 de conectores no fueron ejecutados.

No hubo cambio de código del harness. No se repitió la suite por cambios documentales; la suite de 125 aprobadas y una omisión pertenece a la prueba anterior, no se presenta como nueva validación de estos análisis. Se ejecutaron las verificaciones documentales pertinentes y `git diff --check` antes de publicar.

Corrección de coordinación: la evidencia y respuesta de Workshop dicen once etapas; la matriz contiene **diez**, cubriendo todos los pasos exigidos. Se conserva la evidencia original y se registra el conteo correcto en [verificación integrada](verificacion-integrada.json) y registro de errores.

## Sesiones y commits

| Frente | Commit de la ejecutora | SID ejecutor | SID revisor | Resultado |
|---|---|---|---|---|
| Workshop | `6dd1b56eb9d22cf01c64760b2890a50264022401` | `01a1bcdd-0099-7483-83ab-a10c844b9dbb` | `01a1bce4-3dff-7d82-ace0-00d23bf37a00` | bueno / aceptado |
| Referentes | `dbc146d1db388bbfb7bc5d26f53ff3f2b34b08c4` | `01a1bcdd-0c5a-7023-8b3a-eeefc507ee59` | `01a1bce4-45bd-76a2-a90a-9b31e9fc1da1` | bueno / aceptado |
| Conectores | `486899d8a09b122595327cf3fcef966ed6f8f855` | `01a1bcdd-1833-73b2-9678-0c0d21161dde` | `01a1bce6-9483-7a92-b253-807b644515fc` | bueno / aceptado |

Los tres ejecutores usaron Sol/low, login ChatGPT exigido, `approval_policy=never` y Git privado dentro del perfil acotado. Los revisores usaron Sol/low y read-only. Cada ejecutora hizo su propio commit/push; el coordinador comprobó el remoto, cerró, recogió veredicto, aceptó y liberó la reserva. Integración: avance rápido de Workshop y merges secuenciales de Referentes/Conectores, sin reescribir sus commits.

Se observaron las tres ejecutoras vivas en dos snapshots separados por **36.721 segundos**. Es un mínimo documentado de solape, no un benchmark de CPU ni la duración total. Los cupos se reutilizaron para revisores sin superar tres sesiones vivas del harness. Al cerrar quedan cero sesiones del lote vivas; worktrees limpios retirados, ramas y Git privados conservados. Los 40 archivos con cambios previos del checkout principal conservaron bytes y conjunto.

## Cuota, interfaz y consulta

Cuota semanal observada: 17% antes del lote y 19% en el último recibo de revisión. Saldo adicional cero, sin API keys/compras. Es una cuota compartida con coordinación y otras tareas; la diferencia no mide consumo exclusivo del lote. No se tocaron producción, n8n, Docker, app-server ni servicios.

Las sesiones son ejecuciones CLI del VPS y no chats nuevos creados con la app. La lista de chats de este host devolvió sólo esta conversación; el subagente visible era el auxiliar de coordinación. [Mapa de trabajo](MAPA-DE-TRABAJO.md).

```bash
cd ~/repos/onia-coordinador
H=_investigacion-onia/base-operativa/05-herramientas/scripts/harness.py
python3 "$H" estado
python3 "$H" retomar analisis-workshop-20261108
python3 "$H" retomar analisis-referentes-20261108
python3 "$H" retomar analisis-conectores-20261108
```

Los registros canónicos están en `04-operacion-agentes/tareas/`; los logs privados, en `~/operacion/logs/`. Los recibos por tarea conservan preflight, publicación, cierre, veredicto y aceptación. [Lanzamientos](lanzamientos.json), [snapshot concurrente](tres-ejecutoras-vivas.json), [comprobación integrada](verificacion-integrada.json). Los comandos concretos y el helper de coordinación usan el harness existente; no son otro scheduler.

## Lectura del registro y corte de Sergio

Los campos `comprobacion` de los registros conservan el chequeo previo al cierre y su frase «Falta cotejo cualitativo independiente». Ese cotejo ya ocurrió: el resultado posterior y vigente consta en `revision_independiente`, `aceptacion` y estado `aceptado`. Se preservan evidencias y veredictos originales; no se reescribieron hashes para ocultar el texto previo.

Sergio indicó terminar este lote, avisar y hacer stop; después corregir los problemas y continuar con el encargo de Grokbot. Este cierre respeta ese orden: no lanza el nuevo lote. La revisión auxiliar del cierre confirmó integridad y detectó dos precisiones documentales aplicadas: el límite cuenta sesiones, no todos los procesos hijos, y el chequeo previo debe leerse junto con la aceptación posterior.
