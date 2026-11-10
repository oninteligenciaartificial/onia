# Fábrica de contenido OnIA: desglose punto por punto

9 nov 2026 · 20:45 America/La_Paz · Boss. **Borrador para que Sergio corrija; no se lanza nada a Codex hasta su sí.**
Base: [ONE-MAN-COMPANY-FABRICA-CONTENIDO-20261109.md](ONE-MAN-COMPANY-FABRICA-CONTENIDO-20261109.md) y los dos videos de Euge (video 1 [17:58–28:31](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1078s), video 2 [24:00–26:35](https://youtu.be/xPJbP9yZE1I?t=1440)).

## Qué fábricas muestra Euge y cuáles hacemos

| Fábrica de Euge | ¿Genera ingresos para OnIA ahora? | Decisión |
| --- | --- | --- |
| Idea ganadora | Sí (contenido que vende el workshop) | Se hace ahora |
| Guion | Sí | Se hace ahora |
| Edición de video (sala de montaje) | Sí | Se hace ahora |
| Código (taller de PR) | No directo | Después |
| Automática sin revisión (Leader Summaries) | No; Sergio publica | No se hace |

Regla común de Euge: atomizar hasta el resultado más chico que se pueda evaluar, definir qué lo hace bueno, y ciclo medir → aprender → mejorar.

## Fábrica 1 · Idea ganadora (Boss, en Grok Bot, sin cuota de Codex)

| Paso | Entra | Sale | Quién | Qué lo hace bueno |
| --- | --- | --- | --- | --- |
| 1 Materiales | Cerebro de referentes (03-referentes), CEREBRO-DIARIO, noticias IA 24 h con fuente, comentarios y preguntas reales de Sergio | Lista de materiales del día | Boss | Solo referencias que Sergio sí usa; noticia con fuente |
| 2 Candidatas | Materiales + 5 slots fijos | 20 ideas (4 por slot) | Boss | Cada idea dice slot, gancho y por qué le importa al avatar |
| 3 Público simulado | 20 ideas | Puntaje de 3 personas: dueño de negocio en Santa Cruz principiante, emprendedor joven, profesional curioso de IA | Boss | Se descarta lo que ninguna persona vería entera |
| 4 Crítico | Sobrevivientes | 5 ganadoras (1 por slot), con motivo | Boss | Claridad, prueba, CTA al workshop, sin promesas falsas |

## Fábrica 2 · Guion (Boss)

| Paso | Entra | Sale | Quién | Qué lo hace bueno |
| --- | --- | --- | --- | --- |
| 1 Estructura | Idea ganadora + formatos-onia.md | Gancho (3 s), cuerpo, CTA | Boss | Voseo boliviano, 30–60 s hablados |
| 2 Crítico | Guion | Guion corregido | Boss | Se entiende sin contexto; CTA del workshop en venta |
| 3 Entrega | 5 guiones | 02-contenido/fabrica-diaria/AAAA-MM-DD.md + mensaje a Sergio 07:00 | Boss (rutina diaria) | Listos para grabar en una sola tanda |

## Fábrica 3 · Edición (Codex en VPS/HOMELAB; Boss dispara y revisa)

Pasos de Euge: recibe → escucha → cortar → montar, con agentes en cadena (uno recorta, otro propone imágenes/B-roll, el modelo fuerte termina) y sala de montaje.

| Paso | Entra | Sale | Quién | Qué lo hace bueno |
| --- | --- | --- | --- | --- |
| 1 Recibe | Grabación de la tanda en Drive «1 Entrada» | Archivo en cola privada (fuera de Git) | Boss mueve; Codex recibe | Nada de Sergio en Git |
| 2 Escucha | Video | Transcripción con tiempos | Codex (ASR existente en /opt/onia-asr-pilot-20261105) | Español correcto |
| 3 Cortar | Transcripción + 5 guiones | 5 segmentos, última toma buena, sin silencios | Codex | Si duda, marca para revisión |
| 4 B-roll | Clips de Drive «2 B-roll» | Qué clip va en qué frase | Codex | Clip relacionado con lo que se dice |
| 5 Montar | Segmentos + B-roll | 5 mp4 9:16 con subtítulos y gancho en pantalla | Codex | Legible en celular |
| 6 Sala de montaje | Borradores en Drive «3 Sala de montaje» + comentarios | Versión nueva | Sergio comenta; Codex rehace | Cada comentario se guarda en CRITERIOS.md |
| 7 Aprender | Antes/después de Sergio en Drive «4 Ejemplos» | Diferencias y criterio corregido | Codex | Duración y cortes parecidos a los de Sergio |

El vlog diario no entra: se publica entero sin edición. Publicar siempre lo hace Sergio.

## Plan de esta noche (hasta mañana 10 nov)

1. Sergio corrige este desglose y da el sí.
2. Boss ajusta la rutina diaria de 07:00 a Fábricas 1 y 2.
3. Boss pasa a Codex un PEDIDO solo de la Fábrica 3, pasos 1–5 primero (Sol low, sin subagentes, revisor distinto).
4. Mañana: 5 guiones 07:00 → Sergio graba y sube → Fábrica 3 corta → Sergio revisa.
5. Último: pasos 6–7 (loop de aprendizaje) listos mañana.

Cuota: Fábricas 1 y 2 en Grok Bot; Codex solo Fábrica 3; modelo fuerte solo en la revisión final.
