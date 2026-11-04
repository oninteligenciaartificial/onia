# Mapa del repositorio ONIA

4 de noviembre de 2026. Incluye 82 rutas de la entrega consolidada. Nueve skills propias; ninguna skill nueva por referente. El commit de entrega se consulta en Git. Los datos privados, medios, credenciales, dependencias y perfiles de navegador están excluidos.

## Entrada por necesidad

- [Estado real y siguiente acción](ESTADO.md).
- [Cómo ejecutar y delegar](ORQUESTACION.md), con una skill directora por área.
- [Operar navegador y tareas cloud](cloud/OPERAR.md).
- [Investigación curada: nueve referentes y producción](investigacion/2026-11-04/README.md).
- [Fuentes del día a día](CEREBRO-DIARIO.md) y [panel de Notion](PANEL-DIARIO.md).
- [Evidencia del 4 de noviembre](EVIDENCIA-2026-11-04.md).

## Árbol de esta entrega

```text
.gitignore
AGENTS.md
README.md
_investigacion-onia/
  base-operativa/
    .gitignore
    AGENTS.md
    CEREBRO-DIARIO.md
    ESTADO.md
    EVIDENCIA-2026-11-03.md
    EVIDENCIA-2026-11-04.md
    INICIO.md
    MAPA.md
    ORQUESTACION.md
    PANEL-DIARIO.md
    PLAN.md
    SESIONES.md
    SKILLS-POR-AREA.md
    accesos.md
    arquitectura.md
    auditoria-30-repos.md
    catalogo-repos-2026-11-03.json
    cloud/
      .gitignore
      CARGA-INICIAL.md
      CONFIGURAR-ONIA.md
      INICIO-SESION.md
      OPERAR.md
      README.md
      browser-runtime.cjs
      browser-runtime.test.cjs
      browser.spec.cjs
      install.sh
      meta-inventory.py
      n8n-inventory.py
      package-lock.json
      package.json
      playwright.config.cjs
      start.sh
      test_meta_inventory.py
    compartibles/
      skills/
        automatizar-n8n/
          SKILL.md
          agents/
            openai.yaml
        continuidad-de-trabajo/
          SKILL.md
          agents/
            openai.yaml
        desarrollar-y-verificar/
          SKILL.md
          agents/
            openai.yaml
        evaluar-catalogo-skills/
          SKILL.md
          agents/
            openai.yaml
        mejorar-sistema/
          SKILL.md
          agents/
            openai.yaml
        planificar-dia/
          SKILL.md
        preparar-campana-meta/
          SKILL.md
        preparar-oferta-y-embudo/
          SKILL.md
        producir-video/
          SKILL.md
          agents/
            openai.yaml
    correccion-procedencia.md
    fuentes.md
    investigacion/
      2026-11-04/
        README.md
        alex-hormozi.md
        ali-abdaal.md
        como-operan.md
        enrique-rocha.md
        erik-taveras.md
        formatos-onia.md
        iman-gadzhi.md
        jeff-nippard.md
        justin-welsh.md
        nick-bare.md
        san-munoz.md
        workshop-piloto.md
    orquestacion.json
    recorrido-comercial-inicial.md
    registro-de-errores.md
    reglas-comunes.md
    revision-carrusel-DfQnRTcjCXU.md
    revision-onia-platform.md
    revision-reel-DfBQ1AgOC1S.md
    scripts/
      harness.py
      instalar-skills-locales.ps1
      preparar-cloud.py
      test_harness.py
      test_preparar_cloud.py
      test_trabajo.py
      trabajo.py
    seleccion-y-recorrido.md
```

Este árbol es una instantánea fechada; el listado vigente se obtiene con `git ls-files`. Los chats por área están en SESIONES.md. Leer el índice pertinente y luego los archivos necesarios, sin cargar el árbol completo como instrucciones de cada tarea.
