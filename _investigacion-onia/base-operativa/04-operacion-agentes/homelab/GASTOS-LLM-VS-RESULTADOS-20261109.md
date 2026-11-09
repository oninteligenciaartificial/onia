# Gastos LLM vs resultados — 2026-11-09

Investigación de Boss (America/La_Paz). Sin secretos ni precios inventados como facturados.

## Timeline de cuota semanal (`used_percent`)

| Momento (aprox.) | used_percent |
| --- | --- |
| Dom 8 nov ~11:54 | 7% |
| Dom 8 nov ~18:52 | 34% |
| Lun 9 nov ~00:34 | 46% |
| Lun 9 nov ~01:39 | 53% |
| Lun 9 nov ~08:46 | 61% |
| Lun 9 nov ~13:25 | 64% |

- Reset: viernes 13 nov 22:47 (America/La_Paz).
- Plan: prolite; créditos extra: 0.
- Precio del plan: no visible en la cuenta. Estimación de terceros ~USD 100/mes — **no verificada**.
- Harness (muestra leída): 56 filas; 19 tareas únicas; 33 finalizada; 22 cerrada; 1 fallida.
- Commits: 159 en 7 días.
- Factura Hostinger: no recuperada (timeout).

## Cómo estamos vs cómo debería ser

| Tema | Cómo estamos | Cómo debería ser |
| --- | --- | --- |
| Visibilidad de costo | Solo el % semanal de cuota | Recibo por tarea (modelo, cuota gastada, intentos, resultado) |
| Enrutado de modelos | high/ultra casi por defecto | low para docs/tests; high para diseño; ultra solo para aceptación crítica |
| Gasto vs ingreso | Mucha cuota y aún sin venta | Hasta el 14, la cuota va primero a lo que vende |
| Caché | Sin métrica de hit-rate | Medir y subir el reuso de contexto/resultados |
| ASR / embeddings | CPU en el VPS | En el homelab local; API paga solo para razonar |
| Cerebro / panel | Docs y HTML | Producto de uso diario (guiones, ventas, próximos pasos) |
| Retrabajo | No medido | % de tareas con ≥2 intentos |

## Homelab progresivo (etapas)

Ninguna compra sin el sí explícito de Sergio. Precios de mercado usado 2026, aproximados.

| Etapa | Qué | Costo aprox. | Disparador |
| --- | --- | --- | --- |
| E0 | PC actual + VPS coordinador | USD 0 extra | Hoy |
| E1 | RTX 3060 12 GB usada + SSD 1–2 TB + UPS básico | ~USD 250–500 | Cuando el ASR frene al VPS |
| E2 | GPU 16–24 GB (p. ej. 4060 Ti / 3090 usada) | ~USD 500–1.800 | Cuando haya ingreso estable |
| E3 | NAS + UPS serio + opcional 2.ª GPU | +USD 200–800 | Respaldos, tareas de noche, orquestación completa |

Correr en casa conviene primero para transcribir y buscar en el cerebro. Reemplazar Codex con un modelo grande local exige uso sostenido alto.

## Recibo obligatorio por tarea

En cada recibo (ejecutor y revisor):

- `id`
- `modelo` + `esfuerzo`
- `used_percent` al inicio y al final
- `intentos`
- `resultado` (aceptada / rechazada / fallida)
- `commits`
- `retrabajo` (sí/no o conteo)

No inventar montos en USD.

## Fuentes

- https://learn.microsoft.com/en-us/startups/build/ai/ai-cost-optimization
- https://www.getapipulse.com/blog-ai-startup-api-budget-2026.html
- https://dev.to/sikamikanikobg/cloud-vs-local-the-break-even-point-where-self-hosting-stops-losing-money-4f04
- https://readygpu.com/us/used
