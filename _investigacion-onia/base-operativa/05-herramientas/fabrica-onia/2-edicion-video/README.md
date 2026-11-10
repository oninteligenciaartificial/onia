# 2 · Edición de video

Especificación de la cadena que convierte la tanda grabada en cortes 9:16 con subtítulos, listos para que Sergio revise. Corre en el VPS. Boss no la configura: Codex la implementa cuando Sergio lo autorice (frente 3 del [plan al 13](../../../04-operacion-agentes/PLAN-LISTO-AL-13-20261110.md)).

## Qué hace

Recibe la grabación de la tanda, la transcribe por CPU, propone cortes, inserta B-roll y monta un vertical 9:16 con subtítulos. Las decisiones dudosas se marcan para revisión humana. El vlog diario no entra a esta cadena.

## Cómo lo hace Euge

- Video 1, [17:58–18:53](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1078s): Grok no le alcanza para editar. Muestra ediciones con motion graphics atribuidas a Opus 5.5 (recortes, clips de afuera, gráficos). Eso es su receta, no la nuestra.
- Video 1, [19:08–19:30](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1148s): propone montar esas fábricas en un ordenador persistente más capaz (él cita un servidor cloud tipo Hetzner) pidiéndole ayuda al capataz. No es una cotización ni una orden de contratar ese servidor.
- Video 1, [25:46–25:55](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1546s): en pantalla se ve un montaje «paso 4 de 5» y el aviso de que algo falló. Los pasos que nombra: **recibe, escucha, cortar, montar**.
- Video 1, [24:08–24:47](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1448s) y [26:11–26:19](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1571s): sala de montaje para ver el proceso, comentar «cambiame esto» y pedir otra versión. Enseña con un antes y un después hecho a mano, como si le mostrara el trabajo a un empleado. Si el resultado no coincide, se investiga qué criterio falló y se guarda en el procedimiento.
- Video 2, [25:03–25:34](https://youtu.be/xPJbP9yZE1I?t=1503): entra un video sin editar; un agente recorta de la mejor forma posible; otro propone imágenes para meter; Opus termina la edición y entrega el resultado.

No se copian Opus, Clonify Studio, ElevenLabs ni el servidor cloud pago.

## Cómo lo hacemos en OnIA

Cadena de esta semana, en el VPS, sin GPU:

**recibe → escucha (ASR por CPU) → cortar → B-roll (clips de Sergio; Higgsfield opcional, con créditos y el sí de Sergio) → montar 9:16 con subtítulos (FFmpeg) → revisión humana.**

Boss mueve los archivos entre Drive y el VPS. Codex implementa el script y los tests. Una transcripción con tiempos no equivale a escuchar: hay que marcar frases dudosas, cortes inciertos y problemas de sonido para que Sergio o Contenido los revisen.

**Veredicto infra OnIA: parcial.** FFmpeg y un piloto de transcripción por CPU ya existen en el VPS. Falta el script que recorre la cadena con una pieza real. No se afirma que el piloto reproduzca la edición de Opus.

## Entra / sale

| Entra | Dónde | Sale | Dónde |
|---|---|---|---|
| Tanda grabada (los cinco guiones del día) | Drive [1 Entrada](https://drive.google.com/drive/folders/1OWW5GGfF1GQrXFer7HmLEoIf9sQRGrWp); Boss la copia a la cola privada del VPS `~/operacion/fabrica/entrada/` | Por guion: corte 9:16 con subtítulos quemados y lista de dudas | Drive [3 Sala de montaje](https://drive.google.com/drive/folders/1bZs-7y3BkPm3qDC7vUxqVAt_s5GLbGmA) |
| Clips de apoyo | Drive [2 B-roll](https://drive.google.com/drive/folders/1ogk1iwL3rgr_OKpBV70PdzgSmwAIClot) | Elementos de IA, sólo si hay sí y créditos | Higgsfield (pago). Si no hay sí, se omite |
| Guion e intervalos propuestos | Fábrica 1 / Contenido | Corrección hecha a mano | Drive [4 Ejemplos](https://drive.google.com/drive/folders/1-2dzLYGFGk_zNnii7-Qz2VI__p0JvtHf) y, en texto, `reglas/` |
| Video de prueba o G01 real | Cola privada del VPS; nada de esto va a Git | Recibo de tests y de la pieza procesada | `salida/` de esta carpeta (metadatos y hashes, no el mp4) |

Codex no toca Drive. El usuario del VPS es `onia-codex-worker`; el repo ahí es `~/repos/onia-coordinador`.

## Quién la hace

- **Codex:** implementa el script, los tests y el manual de uso, hasta el 13.
- **Boss:** especifica, mueve Drive ↔ VPS y revisa que la entrega técnica cumpla la lista.
- **Contenido:** propone intervalos y valida que el corte respete el guion.
- **Sergio:** graba, sube a 1 Entrada, revisa sonido e imagen, aprueba y publica.
- El homelab de la PC de casa queda como opción posterior del plan fijado; esta semana la edición corre en el VPS. La laptop que el plan deja fuera sigue fuera.

## Criterio de «bueno»

- Frases sin cortar a la mitad.
- Subtítulos correctos: mismas palabras, tiempos alineados, legibles en un celular.
- Encuadre 9:16 sin texto tapado.
- Sonido revisado por una persona (el ASR no certifica mezcla ni intención).
- El B-roll corresponde a lo que se dice. Higgsfield no inventa hechos ni caras de terceros.
- Las dudas quedan marcadas; no se publican solas.
- El vlog no se recorta en esta cadena.

## Cómo se mide

Al final de cada tanda: piezas recibidas, piezas renderizadas, piezas que pasaron la lista, piezas devueltas y tiempo de espera del render en CPU. No se inventan minutos ni se promete que el ASR de un crudo largo sea instantáneo.

## Qué existe y qué falta

Ya está:

- [audiovisual.py](../../scripts/audiovisual.py): sólo ingesta con ffprobe. No edita, no transcribe, no corta.
- Piloto y scripts de transcripción por CPU: [asr-local/README.md](../../asr-local/README.md).
- FFmpeg está en el VPS (plan al 13 y plan fijado).

Falta el script del frente 3 (el plan fijado lo describe como un `procesar` que hace ASR, corta según un JSON de intervalos y deja 9:16 con subtítulos). Falta probarlo con la grabación real de G01.

## Desde el 14 sin Codex

Funciona si el script quedó con tests y se corre con un comando, sin pedir un modelo. Si no está listo, Sergio edita a mano y esta fábrica queda documentada, no automática.

## Pedido para Codex

Frente 3 del plan al 13. Prioridad después de la venta y de G01. Boss no implementa esto.

- **ID sugerido:** `fabrica-edicion-video-20261110`
- **Rutas exclusivas:** `05-herramientas/fabrica-onia/2-edicion-video/` (el script y sus tests viven aquí; no modificar [audiovisual.py](../../scripts/audiovisual.py) ni el harness).
- **Qué construir:** un comando local que, sobre un archivo de la cola privada del VPS y un JSON de intervalos, haga transcripción por CPU reutilizando el piloto ya existente, corte con FFmpeg, queme subtítulos en 9:16, inserte B-roll si hay lista explícita, y escriba un recibo con dudas (frases inciertas, cortes al medio, sonido no evaluado). Higgsfield queda fuera de este pedido salvo un sí aparte.
- **Criterio de aceptación:** una pieza de prueba (y G01 real cuando exista la grabación) pasa la lista: frases sin cortar, subtítulos correctos, legible en móvil, dudas marcadas. Tests sintéticos cubren JSON inválido, intervalo fuera de rango y rechazo a procesar un archivo etiquetado como vlog.
- **Tests:** Python estándar más FFmpeg ya instalado; evidencia en una carpeta nueva dentro de esta fábrica; sin red, sin Drive, sin publicar.
- **Qué no tocar:** Drive, n8n, rutinas, el plan fijado, G01/G02, secretos, IPs, la PC, Opus/Clonify/ElevenLabs, y no recortar el vlog.
