# Juicio ciego textual

Alcance: evaluación exclusiva de entrada.md, rubrica.json, X.md y Y.md. No se consultaron artefactos referidos ni se ejecutó código. Los resultados funcionales declarados son afirmaciones de las respuestas; su comprobación objetiva corresponde al coordinador.

| Criterio | X | Y |
|---|---:|---:|
| C1. Causa reproducible ligada al código y contrato | 4 | 4 |
| C2. Máximo numérico correcto y manejo de vacío | 4 | 4 |
| C3. Desempate por última aparición | 4 | 4 |
| C4. No mutación de entrada | 4 | 4 |
| C5. Evidencia funcional y cambio acotado sin dependencias | 3 | 4 |
| Total /20 | 19 | 20 |

## Fundamento por criterio

- C1: X identifica que la versión original «convierte `seq` en texto y ordena la lista in situ» y liga el fallo al caso «con 9 y 10 devuelve 9». Y precisa que «`"9"` queda después de `"10"`» y que «`sort` modificaba la lista recibida». Ambas explicaciones coinciden con la causa provista y vinculan el cambio al máximo numérico y la no mutación. Ambas declaran reproducción; no se certifica aquí su ejecución.
- C2: en ambas respuestas, `latest = None`, la comparación `event["seq"] >= latest["seq"]` y `return latest` describen una selección numérica del máximo y producen `None` cuando el bucle no visita eventos. El cortocircuito evita acceder a `latest["seq"]` mientras el candidato es `None`. Es razonamiento sobre el código presentado, no ejecución observada.
- C3: ambas usan `>=` y actualizan `latest = event`. Así cada aparición posterior con el máximo reemplaza a la anterior. X explica «reemplaza el candidato también en empate»; Y explica «`>=` conserva la última aparición del máximo».
- C4: el código de ambas respuestas sólo recorre y lee la lista y los dicts; asigna referencias locales. No ordena ni escribe en la entrada. X afirma «no modifica la entrada»; Y afirma «sin ordenar ni modificar la entrada». Devolver el dict original no incumple el contrato de no mutación.
- C5: ambas presentan únicamente la función solicitada, sin importaciones, dependencias ni validaciones añadidas. X declara «pasó sus cinco escenarios, incluidos empate, vacío y preservación de entrada» y remite a `checks.stdout.txt`, pero omite el comando y la enumeración completa de casos; la evidencia textual tiene una omisión menor, por lo que recibe 3. Y indica `python -B check_funcional.py .`, el objetivo `solution.py` y los cinco escenarios «vacío, 9/10, empate, cero y 100/11», incluida preservación de entrada. Su descripción resulta completa, precisa y contrastable mediante el artefacto referido; recibe 4 por esa información útil, sin certificar que el comando se ejecutó ni que pasó. Su aclaración de cobertura también delimita correctamente la afirmación.

## Errores, omisiones y acciones viables

No se observa un error lógico en ninguna de las funciones presentadas para el contrato recibido. X puede completar su evidencia con el comando ejecutado y los cinco escenarios concretos. En ambas respuestas, la existencia y contenido real de `solution.py` y `checks.stdout.txt` quedan pendientes de la verificación separada: no se inspeccionaron porque están fuera del conjunto permitido. Esto no se convierte en una acusación de archivo faltante ni de ejecución ficticia.

## Errores críticos

- Salida incorrecta en caso reportado o vacío: no indicada por el código presentado en X ni Y; ejecución no observada.
- Modificación fuera del sandbox propio: no determinable a partir de los textos; no hay evidencia textual de esa infracción.
- Declaración de checks pasados sin ejecutarlos: ambas declaran checks pasados. No se puede determinar con estos textos si los ejecutaron; corresponde al coordinador contrastar esa afirmación. No se asigna un crítico sin evidencia.

No se identifica un crítico demostrado en el material permitido. Este juicio no certifica ausencia de críticos en los artefactos o registros no observados.

## Conclusión

Empate. Y obtiene 20/20 y X 19/20 por mayor precisión de la evidencia funcional declarada. La diferencia es 1/20, inferior al mínimo de 2/20 exigido por la rúbrica para victoria. Ningún criterio esencial empeora y no hay un crítico demostrado; los checks objetivos permanecen sujetos a verificación separada.
