# Errores y correcciones de esta entrega

Registro exclusivo de esta carpeta. El registro canónico de errores queda a cargo del coordinador.

## Identificador técnico y límite del harness

En `evidencia/ensayo-01` el adaptador pasó sus veinte controles. El primer puente de prueba pasó `telegram-` más 64 caracteres hexadecimales directamente a `trabajo.decide`. La API rechazó la decisión por su límite de 64 caracteres. El registro aislado quedó en revisión 2 sin decisiones. Sus archivos y tres locks archivados se conservan íntegros.

Se corrigió la frontera en `ensayo-integracion.py`. Verifica el patrón completo del ID técnico y utiliza los 64 caracteres del SHA-256 como ID del harness. El recibo inmutable conserva su ID técnico original. `evidencia/ensayo-02` comprobó escritura de una decisión en revisión 3, revisión vieja, ID repetido y conciliación mediante su fuente. La copia n8n devuelve el mismo recibo seco y mantiene la traducción en la capa del coordinador.

## Consulta documental fallida

La consulta del archivo histórico `packages/cli/src/public-api/v1/handlers/workflows/workflows.handler.ts` en el repositorio oficial devolvió 404. Se usó la referencia REST oficial vigente de workflows para los campos de creación. También falló una ruta de cookbook. La guía oficial Code y Manual Trigger aportaron la capacidad necesaria. Esas consultas fallidas permanecen fuera de la evidencia de importación o ejecución.
