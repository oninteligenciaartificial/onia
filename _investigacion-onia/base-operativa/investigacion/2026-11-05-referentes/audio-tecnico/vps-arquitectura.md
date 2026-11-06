# Diseño propuesto: análisis audiovisual en VPS

Estado: diseño, 5/11/2026. Responsable de ejecución futura: Desarrollo; aceptación de referentes: Jefa. Sergio habilitará el acceso cuando tenga la laptop. Ninguna capacidad, servicio, recurso o nombre propuesto aquí está comprobado en el VPS. La prioridad inmediata sigue siendo terminar referentes con evidencia; este diseño no completa ese objetivo.

## Componentes y límites

- **Ingesta y medios:** reutilizar el corpus autorizado y sus manifiestos, hashes, duración y procedencia existentes en `audio-tecnico/README.md` y el almacenamiento de operación allí referenciado. Registrar origen, versión y derivados; mantener originales inmutables y no duplicar datos privados en Git. Retención, cifrado y capacidad efectiva se deciden tras inventario; borrar temporales sólo conforme a una política aprobada.
- **ASR:** transcribir voz con marcas temporales y confianza cuando el motor las proporcione. No certifica sonidos, emoción ni mezcla; guardar salida y versión sin presentar texto automático como revisión humana.
- **Eventos sonoros:** detectar candidatos de voz, música, efectos y silencios con controles conocidos. No equiparar clasificación a escucha fiable, prosodia o mezcla. Conservar respuestas y errores por modelo y configuración.
- **Video y sincronía:** extraer fotogramas o clips con mapa de tiempos y analizar orden/movimiento según cobertura explícita. Sincronía exige evidencia temporal conjunta de audio y video; ni fotogramas aislados ni ASR la acreditan.
- **Coordinador batch y workers:** cola persistente con estados pendiente, en ejecución, terminado y fallido; identificador, procedencia, intentos limitados, versiones, recursos y error. Trabajos reanudables e idempotentes, cancelables por unidad. No abrir endpoints públicos para las pruebas; acceso privado y mínimo necesario.

Repositorios, commits, modelos, pesos, licencias de código y pesos, dependencias y tamaños quedan **por seleccionar y fijar** después de medir CPU, RAM disponible, disco, GPU, carga y reservas. Gratis no implica que quepan ni que sean fiables. No repetir Eureka, MiDasheng o configuraciones ya rechazadas sin identificar y comprobar una causa corregida. Versiones y hashes acompañarán cada resultado; mantener fallos, incluido silencio, como evidencia.

## Datos e aislamiento

Nombres siguientes son ilustrativos, no infraestructura existente. La separación mínima exigida es **bases de datos distintas**, no esquemas distintos en una misma base:

| Dominio / dueño funcional | Base propuesta | Acceso, red y almacenamiento |
|---|---|---|
| Plataforma / responsable de producto | `plataforma_db` | Usuario y credenciales propios; sólo servicios de plataforma. Conservar instancia existente y su configuración hasta inventario. Volúmenes y respaldos propios. |
| Análisis / Desarrollo | `analisis_av_db` | Usuario limitado a su base; estado de jobs, manifiestos y referencias a medios, no medios binarios por defecto. Worker y coordinador en red interna privada. Volumen y respaldo propios; medios en almacenamiento separado con control de acceso. |
| Automatizaciones y otros usos / responsable de cada servicio | `automatizacion_db` y base distinta por uso cuando corresponda | Usuarios, credenciales, volúmenes y respaldos independientes; sin permisos cruzados por conveniencia. Intercambio por interfaz autorizada y acotada, no acceso directo a la base de plataforma. |

Evaluar una **instancia PostgreSQL independiente para análisis** para no alterar Supabase/Postgres existente: elegirla sólo después de medir recursos y configuración; si no cabe, no asumir que compartir instancia sea seguro. Aun compartiendo instancia, mantener bases, roles, secretos y respaldos separados. Sin puertos de base públicos, privilegios administrativos compartidos ni secretos en Git. Credenciales en mecanismo protegido existente o uno aprobado tras inventario; no copiar credenciales entre servicios. Ninguna migración de producción por defecto: una propuesta específica debe incluir respaldo, prueba de restauración, ventana, verificación y reversión antes de tocarla.

Cada servicio mantiene backup independiente de su base y configuración recuperable; análisis respalda también manifiestos y medios necesarios según política de retención. Cifrar y proteger copias, registrar versión, fecha y destino, y ensayar restauración aislada con comprobación de integridad; un backup no probado no acredita recuperación. No inventar frecuencia ni almacenamiento disponible antes de medir.

## Ejecución posterior al acceso

1. Confirmar host y acceso; inventariar sólo lectura CPU, memoria libre, disco, GPU, carga y servicios/volúmenes/redes activos sin revelar secretos. Establecer reservas y límites explícitos de CPU, RAM, disco, concurrencia y tiempo según medición; si no hay margen, detener la instalación y comunicar la necesidad concreta sin compras ni ampliar plan.
2. Elegir una única ruta compatible, revisar fuentes oficiales, licencia, dependencias y arranque; fijar commit y hashes. Preparar directorio y entorno propios, sin upgrades del sistema, puertos públicos ni cambios en apps existentes. Instalar únicamente tras comprobar margen y aislamiento. Registrar cambios y rutas para reversión.
3. Ejecutar primero silencio sintético con instrucción neutral y sin VAD que lo oculte; conservar la salida incluso si falla. Si pasa, ejecutar controles positivos conocidos y controles de orden/temporalidad antes de aplicar al corpus. Separar pruebas de transcripción, eventos y percepción/mezcla/sincronía; no atribuir una capacidad que el control no mide. Si falla, detener esa ruta y registrar condiciones y resultado.
4. Sólo tras pasar controles relevantes, procesar muestras autorizadas conservando trazabilidad y límites de cobertura. Verificar efectos sobre cargas existentes. Para revertir, detener sólo los procesos propios, retirar sólo los recursos creados para el ensayo tras verificar rutas y dependencias, y preservar evidencia; no tocar datos o servicios ajenos. Si hay incertidumbre, detenerse antes de borrar.

**Aceptación:** inventario y reservas verificadas; bases y credenciales separadas comprobadas; recuperación ensayada; controles pertinentes y resultados reproducibles registrados, sin degradar servicios existentes. Un contenedor activo o una transcripción aislada no demuestran comprensión acústica integral ni cierran referentes.

## Hechos de continuidad

La ausencia de IAB no demostraba ausencia de Computer Use Windows: se inicializó `@oai/sky` y se abrió Chrome, pero su guard detuvo la lectura por no poder determinar la URL. Hay archivos de identidad SSH locales, sin vinculación ni acceso al VPS acreditados. Modelos ejecutados anteriormente produjeron resultados, pero los controles fallidos impiden tratarlos como fiables para el objetivo. No se identificó ni midió el VPS, no se instaló software allí y el acceso sigue pendiente de la acción de Sergio.
