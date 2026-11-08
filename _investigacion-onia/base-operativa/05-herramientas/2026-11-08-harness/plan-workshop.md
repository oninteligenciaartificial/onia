# Plan del workshop (Boss coordina, Codex ejecuta, Sergio aprueba ✋)

```mermaid
flowchart TD
    D["00-decisiones.md"] --> R["Rúbrica clase 1"]
    R --> CH["Chequeo pre-lanzamiento"]
    CH --> S1{"✋ Sí de Sergio"}
    S1 --> P["Piloto: primeros 10 min clase 1"]
    P --> S2{"✋ Revisión"}
    S2 -->|corrige| P
    S2 -->|ok| A["Sesión A: clase 1 (Claude)"]
    A --> B["Sesión B: clase 2 Vender"]
    A --> C["Sesión C: clase 3 Automatizar"]
    B --> REV["Revisora (no edita)"]
    C --> REV
    REV --> S3{"✋ Aprobación"}
    S3 --> V["Sesión D: ventas"]
    V --> I["Integración + GitHub"]
    I --> W["Jue 12 · Vie 13 · Sáb 14"]
```

- Clase 1 sola primero; B y C en paralelo después; ventas (formulario, VIP) en paralelo al piloto.
- Fechas: piloto 8-9 nov, B+C 10 nov, revisión 11 nov.
- Los pilotos del harness terminaron con autorización de Sergio. El primer lote de análisis de Workshop/Referentes/Conectores también quedó revisado y aceptado; no equivale a producir las clases ni aprobar propuestas comerciales. [Resultados y pendientes](../../04-operacion-agentes/evidencias/analisis-lote1-20261108/INFORME.md).

## Tarea chica antes del jueves (aprobada por Sergio 2026-11-08, falta su sí para lanzar)
ID propuesto: referentes-workshop-20261108 · área marketing · ruta 03-referentes/cerebros/ (solo erik-taveras.md, pedro-buerbaum.md, alex-hormozi.md + carpeta propia)
1. Erik Taveras: una clase o workshop público completo + su página de venta (cursos.eriktaveras.com). Qué tomar para clase 1 y para vender.
2. Cierre por DM / privado de Pedro Buerbaum o Hormozi, aplicado al embudo «comenta NEGOCIO → DM → QR».
Rúbrica: fuentes públicas enlazadas; citas con minuto; separar hecho del referente vs propuesta OnIA; no inventar VIP; entregable de 1 página «qué aplicar en el workshop»; commit en GitHub.
