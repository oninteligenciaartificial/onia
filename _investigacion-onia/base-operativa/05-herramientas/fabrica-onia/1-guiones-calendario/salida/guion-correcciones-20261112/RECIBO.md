# Recibo editorial · T04 · 12 de noviembre de 2026

- **Entrega:** [T04 corregido](T04.md) y [fuentes](FUENTES.md). Checkout coordinado con base `a5f3ff2`. La integración al panel queda a cargo de la coordinadora.
- **Consulta realizada:** lectura del T04 manual, formatos ONIA, guía aplicada y fichas de San P1 y Jeff P2, con consulta offline del catálogo de revisión y enseñanza.
- **Comprobación editorial:** el antes y el después conservan las dos entregas y dejan a B dentro del rango. La locución y los planos rotulan el ejemplo y el cierre pide completar una sola nota.
- **Visionado y producción pendientes:** esta sesión consultó documentos. Quedan sin realizar visionado, escucha, ASR nuevo, grabación, cronometraje de locución y prueba de legibilidad sobre video. Los 40–48 segundos son una estimación.
- **Aceptación pendiente:** Sergio debe indicar si autoriza grabar esta versión.

## Cierre de integración y revisión

- Entrega publicada en Git y desplegada en el panel privado desde `dee17d747943bc701166e5df1f997ce734aae620`. La versión editorial vive en la base privada del panel; el texto y sus fuentes están versionados aquí.
- Ejecutora: `/root/guion_real_fuentes`, perfil solicitado Sol Low, sin hijos. Revisora independiente: `/root/revision_contexto_fuentes`; aprobó `dee17d7` después de corregir el metadato T03 de utilidad a marca. No se atribuyen mediciones de consumo ni modelo efectivo sin registros de ejecución.
- Ensayo: `python3 -B /tmp/onia-guion-staging.py /tmp/onia-cierre-infra-operacion-20261111` pasó en base temporal. Integración: `python3 -B /tmp/onia-guion-recorrido.py 8765 /tmp/onia-guion-recorrido-live.json /tmp/onia-cierre-infra-operacion-20261111` pasó contra el servicio real. Estos auxiliares son locales, no un nuevo producto del harness.
- Se guardó la corrección editorial de Codex, se generó una versión privada y se abrió su formulario de corrección. Repetir las mismas solicitudes devolvió la misma versión. Consulta posterior de SQLite confirmó una revisión y una versión para este objetivo; el original permanece guardado.
- Backend autenticado y proxy local: lectura 200; acceso sin credencial al backend: 401. Detalle en [RECORRIDO-PANEL.json](RECORRIDO-PANEL.json). No se acredita una nueva prueba desde iPhone ni PC remoto: este entorno no resolvió MagicDNS y el intento directo a la IP de tailnet expiró. Se conserva la configuración de acceso existente.
- Versión privada: `/version?id=local-c7c81a18728c1f4e0c4fec4d`. Corrección: `/?objetivo=838c398e41066ca39260d48e3d9a198a1817910e6b13306393a7796d02bfe0aa#correcciones`.
- Alcance cerrado: fuente → guion mejorado → revisión independiente → integración → corrección y versión real consultable. Pendiente: devolución/aceptación de Sergio y ensayo de voz. El guardado de una sugerencia para LLM sólo la deja pendiente de coordinación; no acredita un ciclo automático de reescritura.
