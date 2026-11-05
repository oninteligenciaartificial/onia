# Mapa del repositorio ONIA

4 de noviembre de 2026. Mapa documental de la fuente oficial; el listado exacto de archivos y el commit se consultan en Git. Nueve skills propias; ninguna skill nueva por referente. Los datos privados, medios, credenciales, dependencias y perfiles de navegador están excluidos.

## Entrada por necesidad

- [Estado real y siguiente acción](ESTADO.md).
- [Plan continuo oficial por áreas y dirección del Jefe](PLAN.md).
- [Consolidación documental de la sesión local y cloud](continuidad/2026-11-04/README.md), con fuentes, versiones y límites.
- [Jefe, Aprendizaje y chats ejecutores](SESIONES.md).
- [Cómo ejecutar y delegar](ORQUESTACION.md), con una skill directora por área.
- [Operar navegador y tareas cloud](cloud/OPERAR.md).
- [Investigación, referentes, pendientes y producción](investigacion/2026-11-04/README.md), con [Víctor Heras](investigacion/2026-11-04/victor-heras.md), [ampliación consolidada](continuidad/2026-11-04/fuentes-cloud/referentes.md) y [funcionamiento de redes](investigacion/2026-11-04/funcionamiento-redes.md).
- [Aprendizaje: fuentes y ejercicios](continuidad/2026-11-04/aprendizaje.md).
- [Fuentes del día a día](CEREBRO-DIARIO.md) y [panel de Notion](PANEL-DIARIO.md).
- [Evidencia del 4 de noviembre](EVIDENCIA-2026-11-04.md).

Para capacidades y fallos de n8n, navegador, cuentas y modelos, leer [ESTADO](ESTADO.md). El mapa remite a esa fuente y no mantiene un resumen técnico paralelo que pueda quedar desactualizado.

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
    continuidad/
      2026-11-04/
        README.md
        aprendizaje.md
        manifiesto.json
        fuentes-cloud/
          plan-y-resultados.md
          referentes.md
          biblioteca.md
          guiones-y-workshop.md
          demo-d1.md
          video-y-audio.md
          n8n-piloto.md
          launcher-cloud.md
          producto.md
          workshop-ensayo.md
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
        funcionamiento-redes.md
        iman-gadzhi.md
        jeff-nippard.md
        justin-welsh.md
        nick-bare.md
        san-munoz.md
        victor-heras.md
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

Este árbol es una guía fechada; el listado vigente se obtiene con `git ls-files`. Las exportaciones de `fuentes-cloud/` conservan procedencia e historial, incluidas propuestas sustituidas; [PLAN.md](PLAN.md) y [ESTADO.md](ESTADO.md) dirigen el trabajo actual. Los medios enlazados permanecen en sus almacenes cloud. Leer el índice pertinente y luego los archivos necesarios, sin cargar todos los históricos como instrucciones de cada tarea.
