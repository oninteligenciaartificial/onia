---
name: desarrollar-y-verificar
description: Implementa o corrige una función de software con alcance acotado y evidencia de funcionamiento.
---

# Desarrollo y comprobación

Partí del resultado pedido, el repositorio real y su estado actual. Identificá qué comportamiento cambia y cómo comprobarlo. Un pedido claro permite avanzar; reservá las preguntas para decisiones que cambien sustancialmente el resultado.

- Revisá instrucciones aplicables, rama y cambios existentes antes de editar. Conservá trabajo ajeno. Buscá los consumidores y contratos afectados, no sólo el archivo mencionado.
- Para algo pequeño basta un criterio de aceptación breve. Para una función con varias partes, dividí por resultados verificables. No crear un PRD, issue, rama adicional o proceso TDD por costumbre.
- Reutilizá componentes y dependencias que ya existen. No suprimir controles de datos, autenticación o manejo de errores para reducir líneas.
- En un bug, reproducí el fallo y verificá la corrección. Para cambios de dinero, permisos, integraciones o lógica nueva, comprobá también el caso de fallo relevante. Para texto o estilo simple, una revisión directa puede bastar.
- Ejecutá los checks apropiados después del último cambio. Declarar qué comprobación no pudo correr y por qué. No describir una prueba anterior como validación del código actual.
- Entregá cambio, evidencia y límites. Commit, PR y despliegue siguen el encargo vigente; esta skill no los impone.

Referencia conceptual: Matt Pocock (implement/to-spec), Superpowers (diagnóstico/verificación), Karpathy/Ponytail (alcance y reutilización). Redacción propia; no invoca sus paquetes ni copia sus flujos obligatorios. Para contrastar versiones, usar los repositorios originales del catálogo del proyecto.
