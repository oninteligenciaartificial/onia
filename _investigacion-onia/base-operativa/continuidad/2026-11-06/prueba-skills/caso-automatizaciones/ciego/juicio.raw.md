# Juicio ciego: caso automatizaciones

Fuentes examinadas exclusivamente: entrada.md, rubrica.json, X.md y Y.md. Evaluación estática de las respuestas, sin ejecución de controles, integración, workflow ni verificación de atomicidad real. La longitud y el estilo no suman puntos.

| Criterio | X | Y |
|---|---:|---:|
| C1. Deduplicación por texto y carrera SELECT/INSERT | 4 | 4 |
| C2. Reserva/idempotencia e identidad por event_id | 4 | 4 |
| C3. STOP persistente y bloqueo del siguiente evento | 4 | 4 |
| C4. Timeout incierto, conciliación y estados | 4 | 4 |
| C5. Controles normal/duplicado/concurrencia/reinicio y límite sin runtime | 2 | 2 |
| **Total /20** | **18** | **18** |

## X: evidencia y valoración

- **C1, 4/4:** distingue A/B como e1 y C como e2 aunque diga PLAN. Explica que A y B pueden ver ausencia e insertar dos filas por falta de unicidad y reserva atómica. Identifica el historial de S3 como dato del caso y no como ejecución observada.
- **C2, 4/4:** propone «unicidad garantizada por event_id» y reservar atómicamente procesamiento y efecto con clave estable derivada del evento y tipo de operación. B consulta el estado existente, sin otra reserva. La idempotencia del proveedor es condicional y las limitaciones ante falta de consulta/idempotencia impiden interpretar el diseño como una promesa general de exactly-once. Es una propuesta, no una garantía runtime probada.
- **C3, 4/4:** D persiste la baja y bloquea/cancela pendientes; E se registra como independiente, pero su seguimiento se bloquea. Expresa que «PLAN no revoca STOP por sí solo», exige identidad estable de usuario y coordina comprobación de baja con reserva/despacho. Reconoce el límite de efectos ya entregados y la prioridad humana.
- **C4, 4/4:** la fila de reejecución de e1 mantiene resultado incierto, concilia evidencia del proveedor y marca enviado sin reenviar si se confirma aceptación. Sólo permite reintento ante ausencia concluyente y autorización vigente; ante indeterminación deja revisión humana. Enumera estados explícitos y propone un control de aceptación seguida de timeout.
- **C5, 2/4:** A/C aportan el recorrido normal, A/B el duplicado y la concurrencia; también incluye STOP, timeout y dependencias. Declara expresamente controles propuestos/no ejecutados y ausencia de runtime. Sin embargo, falta un control explícito de reinicio: no establece cómo recuperar reservas o un envío interrumpido después de caer el proceso. La reejecución tras timeout cubre una ambigüedad concreta, pero no comprueba persistencia y recuperación tras reinicio. Esta parte requerida hace que el criterio quede parcialmente completo.

**Acciones viables de X:** definir identidad del usuario y contrato del proveedor; implantar unicidad/reserva en el almacenamiento real; persistir STOP; conciliar envíos inciertos y revisar casos irresolubles. Para completar C5, añadir un control de caída y reinicio tras reservar y tras posible aceptación remota antes de registrar enviado, verificando que se conservan baja, identidad y estado, que el duplicado no abre otro efecto y que no se reenvía a ciegas.

**Errores críticos de X:** ninguno de los tres definidos por la rúbrica. No confunde e2 con duplicado, no propone reenvío automático incierto sin conciliación y no afirma runtime probado.

## Y: evidencia y valoración

- **C1, 4/4:** explica la supresión errónea de C por compartir texto con A; describe la carrera de comprobación e INSERT separados y la ausencia de unicidad/transacción. Atribuye las dos filas al antecedente S3 y no a una reproducción propia.
- **C2, 4/4:** exige unicidad por event_id y operación atómica para resolver duplicados y reservar a lo sumo un efecto por evento y tipo. B reutiliza estado incluso en curso o incierto. Condiciona clave de idempotencia a soporte del proveedor y deja la atomicidad concreta pendiente del almacenamiento real; no ofrece exactly-once general ni afirma haberlo demostrado.
- **C3, 4/4:** D establece exclusión persistente y E queda bloqueado pese a su nuevo ID. Requiere vínculo verificable de usuario, coordina consentimiento con reserva y actualización de STOP y propone serialización por usuario. Reconoce el punto de no retorno y la prioridad humana sin suponer autorización para respuestas.
- **C4, 4/4:** enumera recibido, reservado, enviando, enviado, incierto, bloqueado y error. Ante timeout conserva incierto y consulta el estado remoto; sin consulta fiable ni idempotencia deja revisión humana sin reenvío automático. Permite recuperación sólo después de determinar ausencia de efecto y verificar STOP. Su control de timeout después de posible éxito reproduce la condición relevante del fixture como expectativa, no como resultado ejecutado.
- **C5, 2/4:** cubre A/C normal, A/B duplicado y concurrencia, D/E, timeout, entradas inválidas y dependencia fallida; distingue expresamente controles derivados del texto de pruebas ejecutadas. Falta el caso explícito de reinicio y recuperación de estados persistidos ante caída entre reserva, despacho y registro final. La recuperación genérica de una dependencia no sustituye esa comprobación necesaria.

**Acciones viables de Y:** precisar identidad, autorizaciones y conciliación del proveedor; diseñar unicidad y reserva para el almacenamiento concreto; persistir y coordinar STOP; mantener incertidumbre en revisión cuando no se puede resolver. Para completar C5, añadir el mismo control de caída/reinicio y recuperación de reservas y envíos inciertos indicado para X, con expectativas observables y sin atribuir ejecución a esta auditoría.

**Errores críticos de Y:** ninguno de los tres definidos por la rúbrica. No confunde e2 con duplicado, no ordena reenvío ciego tras timeout y no afirma integración ni atomicidad runtime probada.

## Umbral y conclusión

**Empate: X 18/20; Y 18/20.** Diferencia absoluta: 0/20, inferior al mínimo de 2/20. No hay errores críticos ni caída de criterio entre las respuestas; ambas comparten la omisión de reinicio en C5. No procede declarar una victoria. La conclusión evalúa exclusivamente la calidad estática de las propuestas y sus controles, no el funcionamiento de una implementación.
