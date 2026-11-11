# Etiqueta de revisión técnica en la tanda diaria

Al comprobar el resultado real del piloto, la coordinadora detectó que `diario.attach` dejaba todas las tarjetas en revisión técnica pendiente aun cuando el ciclo ya contenía un dictamen bueno. Ahora la etiqueta sólo indica revisión técnica favorable cuando coinciden los commits del resultado, del harness y del dictamen bueno. La revisión editorial permanece pendiente y no concede publicación.

Prueba HTTP de regresión: dictamen bueno del mismo commit, dictamen con cambios, dictamen de otro commit y ausencia de dictamen. Se comprueba la etiqueta renderizada y que las cinco piezas conservan la revisión editorial pendiente. Las seis pruebas HTTP pasaron en 7.587 s con `python3 -B -m unittest -v test_diario`, ejecutado por la coordinadora en el directorio del panel, con salida 0. Son 36 pruebas de ciclo/programación, 6 de HTTP y 25 del generador cubiertas en sus corridas registradas; no se afirma que todas se repitieron en este delta.

La tanda real 3d50b8211f4cc5d86c3dc30994753f18a20cac21 recibió dictamen independiente bueno. Su cierre y comprobación de navegador se documentan por separado, conservando la revisión editorial pendiente. No se activaron servicios, n8n ni canales comerciales. Este delta requiere nueva revisión independiente antes de integrar el flujo.
