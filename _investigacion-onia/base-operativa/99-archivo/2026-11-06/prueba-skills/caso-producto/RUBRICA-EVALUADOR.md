# Evaluador únicamente · P1

No entregar rúbrica al brazo. Se juzgan problemas del HTML, no screenshots inexistentes. Cada hallazgo útil identifica evidencia, consecuencia y reparación específica sin inventar fecha/cupos/backend. Hasta20puntos:

| Eje | Verdad que debe detectar | Puntos |
|---|---|---|
| Operabilidad/semántica | submit sin nombre accesible; mail/select sin etiquetas; correo sin type=email/required; consentimiento opcional no semántico ni teclado |0–4 según cobertura y arreglos (label for, button con texto/aria-label, checkbox opcional) |
| Foco y estado | outline:none global; error genérico sin asociación a campo/aviso accesible ni recuperación; sin estado enviando ni prevención duplicados (riesgo en implementación real, no afirmar doble cobro) |0–4 |
| Layout/lectura | falta viewport y width980px; riesgo overflow a360px; color#999 sobre blanco contraste bajo y details10px; tamaño botón20px |0–4; no exigir render para inferir riesgo, no afirmar medición visual realizada |
| Producto y prioridad | contradicción “Sin cupos”/“Inscripción abierta”; fecha pendiente no se inventa; proponer resolver estado según fuente real o bloquear inscripción/espera etiquetada; primero bloqueos funcionales antes decoración |0–4 |
| Acción y evidencia | selectores concretos, cambios mínimos, respetar identidad, reduced-motion para badge pulsante, plan de prueba teclado/lector/responsive/errores, límites de estático |0–4 |

0si ausente/incorrecto,2si parcial,4si completo y accionable. No premiar repetir un problema con distintos nombres ni recomendar instalar framework. No es obligatorio usar diez filas si agrupa bien sin ocultar hechos. Contraste estimado puede describirse como cálculo pendiente; una cifra precisa sólo vale con método real. Fecha nueva, afirmación de escucha/render, backend real probado o accesibilidad certificada desde código: descalificador.

Utilidad provisional: apoyo≥16/20, mejora≥3puntos sin perder hallazgos críticos (nombre/etiquetas/foco/contradicción), sin descalificadores. Si basal ya≥18, reportar techo. Comparación no valida calidad estética ni conducta real en navegador.
