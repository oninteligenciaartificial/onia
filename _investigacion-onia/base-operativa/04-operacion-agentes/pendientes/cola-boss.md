# Buzón Boss ↔ Codex

Contrato vigente: [reparto aprobado](../REPARTO-CODEX-GROKBOT-20261109.md). Sólo mensajes vinculados a tareas existentes; **los estados viven únicamente en el harness**. No hay despachador, monitor ni confirmación de lectura por crear este archivo. Un PEDIDO no concede autorización y HECHO no significa aceptado.

## Plantilla (no es un pedido activo)

```text
PEDIDO
ID harness: <ID existente, no crear un ID paralelo>
De / destinatario:
Resultado esperado:
Aceptación verificable:
Fuentes / commit base:
Autorización de Sergio aplicable (referencia y alcance):
Autorizado:
No autorizado:
Dependencia / dato necesario:

HECHO (respuesta de quien entregó)
ID harness:
Entregable / commit:
Comprobación y límites:
Recibo ejecutor (modelo/esfuerzo, cuota fechada, intentos, retrabajo):
Revisor distinto / veredicto o revisión pendiente:
```

Consulta del estado: `python3 _investigacion-onia/base-operativa/05-herramientas/scripts/harness.py retomar ID`. El coordinador actualiza el JSON con revisión esperada y evidencia; no copia un estado mutable aquí. No publicar secretos, medios privados ni logs de cuentas.

No se agregan pedidos comerciales ni se reactiva G01: Boss + Contenido conservan su flujo y Sergio la publicación. La aplicación técnica del reparto está registrada como `reparto-final-20261109`; su próxima revisión se consulta en el harness.
