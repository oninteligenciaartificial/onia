# Cola de render del homelab

El VPS registra el ID, ejecuta un intento por pasada y guarda el resultado en su directorio operativo privado. El homelab hace el render por el mismo SSH con huella fijada del piloto. La cola registra la transferencia de trabajos de CPU. Las dependencias, la aceptación y la integración siguen en el harness.

```sh
cd _investigacion-onia/base-operativa/04-operacion-agentes/homelab
python3 -B cola_homelab.py encolar ensayo-render-001
python3 -B cola_homelab.py tick
```

El ID identifica el trabajo. Encolarlo otra vez devuelve el registro que ya existe. Una llamada a `tick` ejecuta a lo sumo un trabajo que esté pendiente, en recuperación o listo para reintentar. Se puede invocar desde el despachador. La prueba no instala una ejecución recurrente.

El estado se guarda en `~/operacion/homelab/cola-cpu-v1` en el VPS. El MP4 se escribe antes de marcar `entregado`, después de comprobar ID, tamaño y SHA-256. El worker conserva cada intento y su salida publicada bajo `cola-cpu-v1` en su directorio privado. El render retiene el lock en FFmpeg mientras escriba, incluso si su padre termina. Una conexión ocupada o interrumpida genera un reintento con espera creciente de hasta cinco minutos. Cuando vuelve el worker, se reutiliza la salida ya publicada. Si el corte ocurrió antes de publicarla, se puede repetir el render y se conserva el intento parcial. Los fallos del worker y los resultados inválidos quedan `bloqueado` para inspección. El CLI indica ese estado con código 1.

## Pruebas

- `python3 -B -m unittest -v test_cola_homelab` comprueba exclusión de pasadas y renders, pérdida de respuesta, recuperación tras persistir los bytes en VPS y rechazo de un hash incorrecto.
- En la noche del 11 de noviembre de 2026, hora de Caracas y La Paz, se ejecutó la cola por el SSH real y se repitió el mismo ID en una segunda conexión. Resultado H.264 de 640 × 360, 48 fotogramas, 2 segundos, 177.670 bytes, SHA-256 `3f830ed502fff99e0e77e85e89e6f091cc31905883e51899e7c974a5eda62906`. La segunda respuesta informó `reutilizado=true`.
- Se descartó deliberadamente la primera respuesta exitosa del SSH en un segundo ensayo real. Quedó en reintento sin MP4 en VPS. Una instancia nueva de la cola recuperó el archivo del mismo ID y lo verificó en el segundo intento, con los mismos bytes y hash. El corte se simuló en el cliente. Se conserva la evidencia privada de ambos ensayos.

La primera operación admitida es `render-sintetico-v1`, con límites de tiempo y tamaño, y un render activo por worker. El uso con archivos de clientes requiere definir su entrada privada e inmutable, su perfil de procesamiento y el tamaño de transferencia. ASR, ejecución programada y pruebas de reinicio o suspensión de Windows siguen como pasos separados. El diseño de capacidad, leases y fallback entre máquinas está en [SCHEDULER](SCHEDULER.md).


## Paso programado comprobado en el VPS

El 11 de noviembre, un temporizador transitorio de usuario invocó una pasada con prioridad `Nice=10`. En un intento se entregó el mismo perfil H.264 de 177.670 bytes, con SHA `3f830ed502fff99e0e77e85e89e6f091cc31905883e51899e7c974a5eda62906`. Otro disparo sobre la misma cola devolvió `sin_trabajo` y se verificó el hash del archivo conservado. El trabajo ya entregado no vuelve a ejecutarse por el reloj.

Para probar un disparo acotado desde este directorio, después de encolar en una raíz privada de ensayo:

```sh
systemd-run --user --unit=onia-homelab-ensayo-cola --on-active=2s \
  --timer-property=AccuracySec=1s --property=Type=oneshot \
  --property=TimeoutStartSec=80 --property=Nice=10 \
  /usr/bin/python3 -B "$PWD/cola_homelab.py" --root "$HOME/operacion/homelab/cola-ensayo" tick
```

Usar un nombre de unidad nuevo si existe el anterior. En el primer disparo systemd ignoró `RuntimeMaxSec` con `Type=oneshot`; la repetición empleó `TimeoutStartSec`. Se validó el resultado desde el journal y el artefacto, ya que la unidad transitoria se descarga al acabar. La recurrencia permanente y la admisión de otros perfiles siguen pendientes.
