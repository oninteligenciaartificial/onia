# Una grabación → cinco piezas → dos formatos

El script reutiliza el editor y ASR existentes. Contenido/Boss preparan cortes explícitos sobre la grabación de Sergio; los tiempos siguientes son **ejemplo**, no decisiones sobre una grabación real. El vlog queda excluido.

Manifest privado de ejemplo (ampliar piezas T01–T05 con tiempos reales, una entrada común):

```json
{"version":1,"entrada":"tanda.mp4","transcripcion":"texto-revisado.json","piezas":[{"id":"T01","tipo":"reel","intervalos":[{"start":0,"end":10}],"broll":[]}]}
```

Si se omite transcripcion, ejecuta ASR una vez para todo el lote y conserva ese resultado. Después cada pieza usa el mismo texto para ambos formatos. Si los cortes atraviesan frases, rechaza el montaje y requiere ajuste de los intervalos o la transcripción; no inventa tiempos ni palabras.

Desde la raíz del repo:

```sh
D=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/2-edicion-video/trabajos/fabrica-edicion-video-20261110
python3 -B "$D/lote.py" --plan "$HOME/operacion/fabrica/entrada/tanda-plan.json" --salida "$HOME/operacion/fabrica/entrada/tanda-salida-nueva"
```

El padre de salida debe existir; el destino debe ser nuevo. `--preview` genera 360×640 y640×360; por defecto720×1280 y1280×720. El programa procesa en serie con los hilos CPU acotados del editor. No se añade scheduler ni se sube el límite de sesiones. No descarga modelos, sube Drive ni publica.

Una interrupción conserva el lote parcial. Consultar `lote-reporte.json` y los reportes por pieza; no usar piezas de un lote fallido sin revisión. Nunca repetir sobre el mismo destino ni borrar la transcripción para forzar otro ASR. Si se necesita una nueva corrida, aportar como transcripcion el JSON anterior cotejado y elegir salida nueva.

Boss traslada los resultados a Sala de montaje con el acceso que tenga autorizado. Tener este comando no prueba su ejecución desde la llave restringida del puente; la operación autónoma sin Codex sigue pendiente de comprobar. Contenido/Sergio revisan voz, palabras, sincronía, encuadre y sonido; el estado de salida siempre conserva revisión humana pendiente.

Pruebas: suite existente ampliada12/12 pasó, con ASR real offline de voz sintética, cortes/B-roll/audio/geometría, salida vertical/horizontal y rechazo de salida ocupada. Además una prueba del lote con dos piezas y cuatro renders pasó: ASR simulado invocado sólo una vez, para verificar reutilización. Total13 casos ejecutados. Material real y calidad editorial aún pendientes.
