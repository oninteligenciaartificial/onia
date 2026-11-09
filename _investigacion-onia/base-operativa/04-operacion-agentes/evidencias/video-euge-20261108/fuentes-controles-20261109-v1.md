# Fuentes primarias del diagnóstico de controles

Consultadas el9nov2026, aproximadamente11:26UTC. No se instaló ni cambió configuración por estas referencias.

- [Formatos publicitarios de YouTube](https://support.google.com/youtube/answer/2467968?hl=es): distingue anuncios saltables, no saltables y consecutivos. Usar sólo el control normal visible y habilitado si existe; su ausencia no prueba fallo del detector. No todos los anuncios admiten omisión.
- [Solucionar problemas de vídeos de YouTube](https://support.google.com/youtube/answer/3037019?hl=es): enumera comprobaciones de conexión, calidad, sesión, compatibilidad del navegador y extensiones. Es una lista general; no establece la causa de nuestros403. Este encargo no ejecuta sus sugerencias de borrar cookies, reiniciar dispositivo o instalar software.
- [Video solicitado por Sergio](https://www.youtube.com/watch?v=JuAQILH7dkQ): destino único autorizado. Tener una cuenta/perfil disponible no acredita reproducción completa ni análisis de audio.

Prueba elegida: comprobar controles visibles, transición anuncio→contenido y avance posterior al corte previo~44–50s. El código anterior aguardaba publicidad y pulsaba Play, sin usar el control de omitir. El cambio no permite saltos forzados del reloj, interceptar respuestas reales ni esquivar verificaciones de acceso. Resultado real en recibo separado.
