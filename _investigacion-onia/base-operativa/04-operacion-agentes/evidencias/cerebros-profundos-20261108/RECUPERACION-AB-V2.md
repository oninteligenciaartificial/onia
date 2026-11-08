# Recuperación de cobertura A/B · candidatos públicos filtrados

8nov2026. [Inventario de posts principales](posts-publicos-alternativos-v2.json), obtenido sin login/cookies mediante `https://www.instagram.com/<cuenta>/embed/`. Se decodificó el JSON contenido como cadena del HTML; se recorrieron sus posts principales excluyendo subpiezas internas de carruseles del conteo. La primera expresión que buscaba JSON sin desescapar no encontró nodos; no se tomó como ausencia de videos.

- Erik:5posts declarados GraphVideo, de `eriktaveras`. Tiene1preview ya analizada; tres clips completos adicionales podrían cerrar mínimo4 si se obtiene contenido.
- Enrique:6posts GraphVideo, de `soyenriquerocha`; necesita4completos.
- Heras:3posts principales GraphVideo, `DYur-tjvboE`, `DX4rykXv0ia`, `DXzUw8jthB3`, de `victorherasemprendedor`, perfil citado en ficha comercial del repo. Más1VSL cotejada podrían completar4. Los otros códigos pertenecen a carruseles y no se inflan como piezas independientes. Verificar identidad con la fuente comercial propia antes de atribuir.
- San:4posts GraphVideo de `sanmunoz.ia`, perfil citado en ficha comercial. Tiene3videos completos del corpus; falta1pieza nueva completa.

GraphVideo sólo clasifica metadata: estas piezas siguen pendientes de identidad final, medio, contenido, tiempos y5respuestas. El principal retoma al hijo correspondiente, con un escritor por archivo. Se admite ASR local breve y secuencial con herramientas/modelo ya instalados; no instalaciones, modelos nuevos, sesiones adicionales, APIpaga, cookies privadas ni bypass. [Alcance de recuperación](RECUPERACION-B.md).

Rutas privadas de trabajo conservadas: `/tmp/grok-public-<cuenta>-embed.html`; el HTML no se publica para evitar ruido y tokens efímeros. La evidencia compartible es este inventario, URLs y método. Si ya no responde igual, registrar el cambio y mantener los límites. Usar estas entradas en la próxima retoma del ejecutor original; no abrir un segundo escritor mientras siga activo.
