# Consolidación de onia

Estado: implementación revisada técnicamente, lista para publicar y probar en Cloud. No usar esta nota como certificación de publicación, continuidad Cloud o uso móvil.

Autorización: Sergio, chat “Explicar cómo funciona un harness”, turno 01a1b23b-288c-7853-9b84-9285f4dce5ae. Integración: 01a1b221-dbd1-7b10-aada-a26094e04705; revisión independiente: 01a1af41-1ce0-7b72-a888-7fd658396b4a.

Base anterior: 7d26f84d82c138335727735e158df7b904e91582, onia/master. onia-harness permanece intacto como referencia.

Cambios: registro schema2 compatible con lectura v1 y migración explícita; inventario acumulativo de evidencia; revisión esperada; briefing canónico recuperable; tarea compartible única en Git; entrega separada de aceptación; reglas generales y procedimiento separados de contextos históricos conservados con hashes.

Comprobación local: 53 tests, 8 omisiones por symlink Windows, sin fallos; skill continuidad validada y enlaces de documentación comprobados. Revisión independiente en WSL/Linux: 53 tests, cero omisiones, OK, 10.189 s, salida 0. Comando: wsl --exec python3 -B -m unittest discover -s /mnt/c/dev/proyectos/_investigacion-onia/base-operativa/scripts -p 'test_*.py' -v. Es Linux local, no Cloud.

La revisora confirmó 21/21 archivos ajenos intactos, 3/3 snapshots con hashes y contenido equivalente al commit anterior normalizando EOL. Dictamen favorable del conjunto staged de 30 archivos, con dos aclaraciones documentales aplicadas: comandos completos de Start skill y aislamiento de tareas de código paralelas. SHA256 de trabajo.py revisado: 96ade95dd1ef51827c09d7be90b1b7e36e644f6f9808092c823e990ca000d5ee. git diff --cached --check aprobado; atributo CRLF limitado al histórico.

El piloto usará únicamente datos ficticios; B recuperará ID/commit/ubicación, sin recibir el objetivo completo ni la respuesta esperada en su prompt. Commits, identidades A/B y resultados se registrarán al observarlos. Sergio autorizó explícitamente crear B en este chat; A será la prueba Cloud existente 01a1b238-b446-777a-93c0-e31f4034301f.
