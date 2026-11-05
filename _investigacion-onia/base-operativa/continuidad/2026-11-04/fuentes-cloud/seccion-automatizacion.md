# Archivo documental: 5 Chatbot y automatización

> Consolidado por autorización de Sergio. Fuente: [Page original](https://chatgpt.com/space/page_8984a682f49c8191bf368995e7b566ed), secuencia **1**, actualizada 2026-11-04T20:52:21.192772Z. Este archivo conserva evidencia y borradores de esa fecha; **no es un segundo plan activo**. Las decisiones vigentes están en [PLAN](../../../PLAN.md) y los resultados en [ESTADO](../../../ESTADO.md). El texto histórico que diga «vigente», «STOP» o «no modificar Git» describe su momento original y no reemplaza la consolidación autorizada.

Los enlaces a medios/descargas se abren en la Page de origen; esos binarios permanecen en cloud. Esta copia no los incorpora ni vuelve a ejecutar sus pruebas.

---

**4 de noviembre de 2026 · v1.1 · Practicar integración.** [Biblioteca de marca](biblioteca.md).

**Resultado esperado:** saber qué recorrido está probado y qué falta antes de operar. **Entrada:** [cierre n8n accesible, sección «Piloto integrado 4 noviembre»](n8n-piloto.md), [CLI cloud 401](launcher-cloud.md), [B1, conversación propuesta](referentes.md) y [ESTADO](https://github.com/oninteligenciaartificial/onia/blob/master/_investigacion-onia/base-operativa/ESTADO.md). **Responsable:** Automatizaciones para runtime; este chat enlaza la evidencia. **Salida:** matriz evento → identidad única → ejecución → entrega → persistencia → reintento → resultado, con adaptadores reales/simulados. **Prueba para avanzar:** mismo evento repetido o concurrente no duplica lead, entrega o ingreso; el recorrido real autorizado se verifica extremo a extremo.

# Estado informado por coordinación

**Cierre accesible leído por coordinación:** run SYNTH_BRAND_3a7d612c52fb, 60/60 checks HTTP; una carrera concurrente duplica dos filas y tres flujos permanecen inactivos. Meta simulado; 15 tests SQL aislados no integrados. La fuente principal es [«Piloto integrado 4 noviembre»](n8n-piloto.md); la otra página de cierre devolvió page_read_forbidden a coordinación y no se usa como fuente única. n8n API y Notion conector funcionan según pruebas previas; n8n→Notion no integrado. Estas APIs no se repitieron aquí.

Instagram no conectado; Ads vencido. CLI→cloud devuelve 401 en la evidencia existente. No hay scheduler diario ni launcher automático comprobado; sí trabajos cloud supervisados. Un chat abierto no mantiene un servicio permanente.

**Propuesta de control:** guardar IDs de evento/transacción y resultado de reintentos, separar aceptación del evento de entrega real y comprobar recuperación tras fallo. Los mocks deben quedar rotulados en cada resultado.

**Próximo trabajo independiente:** preparar [B1 con fixtures privados](referentes.md), contrastarlo con [W1 y la demo D1](referentes.md) y registrar incertidumbre, duplicación concurrente, STOP persistente y derivación humana. No requiere esperar el ensayo humano de la oferta. Separar ese prototipo de la corrección integrada del runtime n8n, que sigue pendiente. Sin activar workflows, cuentas, mensajes ni publicaciones reales.

