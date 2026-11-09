# Integración de la revisión nocturna

El informe documenta intentos reales previos y sus limitaciones. Los bytes originales se conservan en `*.antes-revision.*`; el recibo histórico los coteja por hash y no se reescribe. `ejecutar.py` y `reproduccion.cjs` incorporan correcciones posteriores solicitadas por el revisor independiente.

- Nunca etiquetar este muestreo como visionado completo: el resultado con imágenes siempre es `parcial`. `fin_indicado_por_reproductor` sólo registra una señal de fin/reloj, sin probar continuidad ni escucha. `visionado_completo_acreditado=false` y `audio_analizado=false` son explícitos. La regresión simula salto0.821→1802.900s y exige parcial.
- Si Node termina dejando `muestra.json` en_curso, conservarlo y escribir `salida.json` con estado efectivo terminal, rc, diagnóstico, fecha y hash del manifiesto. Timeout/interrupción también quedan separados.
- No se repitió el video real tras estas correcciones. La tarea de visionado sigue en_espera. Código probado con clips y perfiles sintéticos, no solución a los HTTP403.

Desde la raíz del repo en el VPS, con las dependencias previamente instaladas:
```bash
python3 -B _investigacion-onia/base-operativa/05-herramientas/video-euge-20261108/nocturno-20261109/probar.py
```

Los tests generan archivos sintéticos en /tmp y los conservan; sólo finalizan su Xvfb/Chromium propios. No tocan el perfil real. El comando `ejecutar.py` sí pide el lease del perfil real y no debe ejecutarse por defecto al revisar. El helper tiene URL fija y requiere el gestor existente del checkout coordinador; no es un analizador universal ni un servicio instalado.

El recibo `salida.json` se escribe después de restituir el visor: si esa restitución falla, el gestor deja diagnóstico/estado para recuperación y no se garantiza ese recibo terminal. La prueba unitaria usa137 como código de shell; Python Popen puede observar-9 ante SIGKILL.
