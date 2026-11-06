# Integración de apoyos de terceros · 6/11/2026

Fuentes recuperables y hashes por archivo en [MANIFIESTO.json](MANIFIESTO.json). Seis paquetes, nueve claves; la asociación del catálogo Agent Skills/Addy sigue provisional. Copias MIT o Apache 2.0 con licencias originales; adaptadores ONIA separados de originales. Sin bootstrap, instalación de dependencias ni activación automática. Las instrucciones de Sergio, ONIA y del entorno prevalecen sobre fuentes externas. `research` conserva referencia a agente de fondo, sujeta a las reglas de delegación aplicables; el handoff usa adaptador ONIA en lugar de temporal exclusivo. Superpowers conserva TDD como referencia, no obligación global.

| Área | Apoyos seleccionables adicionales |
|---|---|
| Marketing | Cuatro generales; `tercero-marketing-humanizer` |
| Video | Cuatro generales; `tercero-visual-hyperframes-plan` |
| Desarrollo | Cuatro generales; `tercero-superpowers-debug`, `tercero-superpowers-verify` |
| Automatizaciones | Cuatro generales; debug y verify para software cuando corresponda |
| Organización | Cuatro generales, además de apoyos propios existentes |
| Producto | Cuatro generales; debug, verify y `tercero-visual-uiux` |

Generales: `tercero-matt-research`, `tercero-matt-writing-agents`, `tercero-matt-handoff-onia`, `tercero-addy-context`. El UI/UX quedó sólo en Producto porque el caso entregado se refiere a revisión de interfaz; no se amplió a Desarrollo sin caso. Para incorporar al briefing usar `preparar ... --apoyo CLAVE`, repetible; sin selección sólo se enumera. Ninguna clave tercera puede ser directora. `retomar` devuelve el briefing con selección. No se crean nuevas áreas ni chats para Jefatura o Aprendizaje.

Verificación final: 26 tests de harness/trabajo sin fallos, 1 omitido por symlink Windows; incluye las seis áreas, selección explícita, retoma en proceso separado, rechazo de apoyos ajenos y de todas las entradas terceras reales como directoras. `harness.py doctor`: 30 rutas presentes, cero errores. Se verificaron 74 archivos originales aportados por Marketing/Video contra sus manifiestos y 14 archivos generales/desarrollo contra snapshots; recursos requeridos y licencias presentes. La consulta es desde ruta local del repo; no prueba catálogo nativo ni disponibilidad cloud. El instalador `instalar-skills-locales.ps1` no se modificó ni ejecutó; no se escribieron `.agents` o `.codex`. No hubo ejecución de scripts externos, test A/B, instalación de motores, render o publicación; estructura no demuestra mejora conductual. Ensayos de calidad corresponden a Aprendizaje.

Comprobación independiente de Jefa: se copiaron manifiesto, scripts, fuentes y recursos requeridos a un directorio temporal aislado, sin copiar el `operacion/` original ni utilizar las skills globales de Codex. `doctor` pasó y se preparó un briefing con apoyo explícito para cada una de las seis áreas; las seis entradas seleccionadas se leyeron desde la copia. La copia temporal se retiró después de comprobar que su destino permanecía dentro del directorio autorizado. Esto comprueba selección y lectura portables; no ejecuta el buscador UI/UX, el motor de video ni una instalación de la app.
