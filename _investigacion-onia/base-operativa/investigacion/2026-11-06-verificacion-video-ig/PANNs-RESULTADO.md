# PANNs: resultado de la prueba

6 de noviembre de 2026 · Resultado cerrado y revisado.

**Sirve como señal auxiliar experimental de actividad de habla en las entradas medidas.** No queda aceptado como detector acústico validado ni como evaluador audiovisual integral de reels.

Se completaron seis inferencias offline: silencio digital, voz flite «one two» y cuatro ventanas del mismo remux de Cormac: [0,10), [10,20), [20,30) y [30,37,78). Cobertura: **37,78 s de audio y 0 s de imagen**. Los controles proceden del generador; no son audición humana ni evaluación retenida independiente. No se utilizó VAD.

| Comprobación congelada | Resultado |
|---|---|
| Máximo Speech: voz > ceros | 0,23548 > 0,00205 |
| Media Speech: tramo con voz > silencio final | 0,21711 > 0,02107 |
| Cormac | Speech supera Music en las cuatro ventanas; máximos 0,71342 y 0,01263 |

Los scores no son probabilidades calibradas. Un score bajo de Music no demuestra ausencia de música. No se validaron umbrales, falsos positivos, recall, efectos, fronteras exactas, palabras, prosodia/emoción, mezcla ni sincronía. La malla de 10 ms es interpolada; no acredita esa precisión temporal.

Cada entrada mantuvo CPU1/workers1/batch1, AS3 GiB y CPU/wall de 120 s, con red bloqueada y checkpoint local explícito. Máximo por entrada: 27,13 s; RSS máximo **muestreado**, 1.267.875.840 B. Preparación acumulada: 194,60/300 s y 678.616.455 B de respuestas HTTP, incluida metadata; overhead TLS/IP no medido. Grupos propios vacíos y límites del padre restaurados.

PANNs 0.1.1 y su MIT quedaron verificados; se conserva el aviso literal Google/AngularJS. Pesos Zenodo v3, CC BY 4.0, SHA256 `dd3b4043a87d4ec13df8082c0fcfee3fb5084151808e47e060987a95eabdd142`. CSV oficial AudioSet: generación 1488737428851815, 527 clases únicas, SHA256 `cdd1049833c4b86127c2773ac0d14a2754b6a6d0d1798002ed5c66e699708429`.

La revisora cotejó originales y confirmó este cierre parcial. [Recibo final](panns-cloud-setup-v3/final-result.json), [recursos](panns-cloud-setup-v3/entry-resources.json), [scores por segundo](panns-cloud-setup-v3/Cormac-Speech-Music-1s.csv) y [revisión](../../continuidad/evidencias/capacidad-audiovisual-001/panns-revision-v1.json). Los 21 archivos del manifiesto se copiaron y verificaron localmente. El ZIP con curvas completas de 527 clases permanece en el laboratorio Cloud: no se copió a PC, publicó ni acreditó persistencia permanente.

No se ejecutan más ensayos en esta unidad. El objetivo audiovisual integral continúa pendiente; cerebro y plan Cloud se tratan después desde coordinación.
