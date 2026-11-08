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
- Pendiente: pausar prueba paralela de 3 sesiones de Codex (espera sí de Sergio).
