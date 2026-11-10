# Registro delegado: fabrica-codigo-pruebas-entregas-20261110

10 noviembre 2026, 17:45 La Paz. Autorización: Sergio (17:33): «decile a Codex que haga las pruebas y yo mismo verifico si lo hizo bien», sobre lo documentado hoy ([bitácora Boss](../BITACORA-BOSS.md), entrada 17:40). Regla vigente (17:31): cada canal se documenta y prueba de punta a punta antes de darse por listo. Sólo pruebas y reporte; no habilita producción, n8n real, envíos, publicaciones, pagos ni instalaciones.

```onia-pedido-v1
{
  "id": "fabrica-codigo-pruebas-entregas-20261110",
  "fabrica": "codigo",
  "esfuerzo": "high",
  "objetivo": "Probar de punta a punta, en el entorno del VPS y sin efectos externos, las entregas listadas en 04-operacion-agentes/BITACORA-BOSS.md (entrada 10 nov 17:40), sobre su commit exacto: fabrica-edicion-video-20261110 (9c9a8a0: las 11 pruebas, incluida la ASR con ~/asr/venv), fabrica-chatbot-whatsapp-20261110 (fbc8747: sus tests y flujos del bot con texto, audio e imagen simulados, active=false), guiones-tanda-20261111-v2 (0a710ac: coherencia de guiones-panel.json con T01–T05, nombre «Claude de 0 a 100: tu negocio con IA», CTA y palabra clave por pieza), y las cadenas/canales de DISENO.md (bf1c65f) y ANALISIS.md (46a2853): para cada canal (comentarios y DMs de IG/Facebook, WhatsApp workshop, WhatsApp ONIA Platform, Meta Ads, guiones, montaje, panel, código) indicar qué está documentado, qué se puede probar ya y probarlo con datos ficticios, y qué no se puede probar todavía y por qué. Los tipos de anuncio y guion son lista abierta: no limitarse a los nombrados. No modificar las entregas probadas, ni producción, n8n real, envíos, publicaciones, pagos, instalaciones, PC, secretos o QR reales.",
  "entregable": "En la ruta asignada: PRUEBAS.md con una tabla por entrega y por canal (prueba, comando exacto, commit probado, resultado pasa/falla/no probado, motivo), las salidas de los comandos en archivos de evidencia, un script reproducible para que Sergio repita las pruebas, y RECIBO.md con ID, modelo, esfuerzo, cuota con fechas, intentos y commits; si un valor no se conoce, marcar unknown; no inventar USD. Declarar qué quedó sin probar y qué hace falta para probarlo.",
  "aceptacion": "Cada resultado trae comando y salida verificables y el commit exacto probado; nada se marca como probado sin evidencia; cada canal de la bitácora aparece con estado pasa, falla o no probado más su motivo; ninguna entrega probada cambia; sin secretos, IPs, QR ni efectos externos. Revisor distinto del productor, sobre el commit exacto. Sergio verifica él mismo el resultado; esta entrega no equivale a aceptación. Commit y push en la ruta asignada; declarar faltantes."
}
```

Entrega técnica no equivale a aceptación. Los estados se consultan exclusivamente en el harness.
