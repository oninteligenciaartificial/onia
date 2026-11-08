# Juicio ciego P1

Evaluación limitada a entrada.md, fixture.html, rubrica.md, X.md y Y.md. No se ejecutó ni renderizó el fixture. No se verificó backend ni se certifica accesibilidad completa. No se atribuyen condiciones experimentales a X o Y.

| Eje | X | Y | Fundamento |
|---|---:|---:|---|
| Operabilidad/semántica | 4 | 4 | X §§3,4,6 e Y §§3,4,6 detectan nombres ausentes, etiquetas, correo y tema sin validación, y consentimiento sin semántica ni teclado. Proponen etiquetas asociadas, correo obligatorio, botón con texto y checkbox opcional. |
| Foco y estado | 3 | 3 | X §§2,5,7 e Y §§1,3,5 detectan outline:none, error genérico sin anuncio/asociación y recuperación ausente. Ambos proponen estado de envío y recuperación, pero ninguno explicita prevención de envíos duplicados mientras se procesa una solicitud real. |
| Layout/lectura | 4 | 4 | X §§7–9 e Y §§4,7,8 cubren viewport ausente, ancho fijo, riesgo móvil, texto #999 sobre blanco, detalles de 10px y botón de 20px. No afirman haber medido la presentación. |
| Producto y prioridad | 4 | 4 | X §1 e Y §2 señalan la contradicción de disponibilidad, preservan la fecha pendiente y requieren fuente real para resolverla. Los bloqueos funcionales preceden a movimiento y lectura. |
| Acción y evidencia | 4 | 4 | Ambos aportan selectores, consecuencias, reparaciones mínimas y comprobaciones posteriores de teclado, lector, responsive y errores. X §9 e Y §9 atienden reduced-motion y conservan la identidad. Los límites estáticos están expresos. |
| **Total** | **19/20** | **19/20** | **Empate.** |

## Críticos y descalificadores

Los cuatro críticos se conservan en ambos: nombre del botón (X §4; Y §4), etiquetas (X §4; Y §3), foco (X §7; Y §5) y contradicción (X §1; Y §2). Ninguno inventa fecha, afirma render o escucha realizados, prueba un backend real o certifica accesibilidad. Sin descalificadores.

## Hechos, omisiones y viabilidad

El código confirma `*:focus{outline:none}`, ausencia de etiquetas y nombre textual del botón, `main` de 980px sin viewport, y un manejador que siempre cancela el submit y escribe el mismo error. Ambos informes separan esos hechos del aspecto exacto pendiente de render. La contradicción de cupos no puede resolverse con este material: exigir la fuente del producto es correcto. La propuesta de Y §2 de un estado pendiente sin prometer inscripción es una medida provisional viable; no demuestra que ese sea el estado comercial real. X §1 deja la decisión pendiente sin inventarla.

La omisión común relevante es impedir solicitudes repetidas durante un envío real. Una reparación viable sería bloquear temporalmente nuevas activaciones durante el estado pendiente, anunciar dicho estado y restaurar la acción tras error; comprobar activación repetida y recuperación con respuestas controladas. Esto es trabajo futuro, no un fallo de backend probado en el fixture.

## Conclusión

X e Y superan individualmente el umbral original de 16/20. La diferencia es 0 puntos: no hay mejora de al menos 3 puntos. Ambos están en techo (≥18); cualquiera que sea la asignación basal, corresponde reportar techo y ausencia de mejora demostrada. Se conservan todos los críticos. El empate no valida estética ni conducta real en navegador.
