# TANDA-01 y prueba local · 4 de noviembre de 2026

Registro de ejecución posterior a 7d2836b. Los chats por área se conservan; no se crearon sesiones nuevas. Coordinación local recuperó los resultados. Esta tanda no vuelve operativa toda la empresa.

## Entregas reales

| Área | Resultado | Límite y siguiente acción |
|---|---|---|
| Transferencia | Jefe exportó 21 archivos originales a JSON UTF-8. Coordinación verificó 21 hashes, rutas seguras y hash del conjunto. Desarrollo recuperó el mismo paquete. | Fuente JEF-IMPL-001; no reconstruir ni asumir que su SQLite equivale a n8n. |
| Workshop | [Guía completa](workshop-ensayo.md), [hoja P01](alumno-p01.md) y [hoja P02](alumno-p02.md). QA independiente aprueba preparación para dos ensayos supervisados. | No compartir guía con alumnos: contiene soluciones. 45 min/pase es presupuesto; no duración, precio o demanda validados. Sergio acuerda voluntarios/horarios y facilita; Marketing coteja registros reales. |
| Web W1 | Chromium cloud: desktop 1440×900 y móvil 390×844, tres preguntas con teclado/estado, instrucción visible, Kit con bytes/nombre exactos, cero solicitudes externas y sin overflow horizontal. Coordinación inspeccionó ambas capturas. | Copia privada, accesibilidad básica; no despliegue, IA conectada ni checkout. HTML recuperable en Page. |
| n8n | Adaptador JSON inactivo y 6 checks locales de estructura/normalización. Metadatos de 112 workflows y dos credenciales PostgreSQL inspeccionados. | Carrera Get+Insert sigue abierta; no integración SQL runtime. Ninguna base de prueba acreditada. Administrar destino/rol exclusivo antes de ejecutar ensayo; no usar credenciales dental/WhatsApp por inferencia. SQL de creación/limpieza propuesto, no ejecutado. |
| Video D1 | Composición de 40 s y guion guardados. Dos VMs reprodujeron EPERM al crear hijo Node; Desarrollo lo reprodujo sin HyperFrames. | D1 sin MP4. Causa administrativa exacta desconocida; no seguir repitiendo contra el mismo bloqueo. Recuperar composición como texto y ensayar en ejecutor permitido. |
| Producto | SHA a0488f0 confirmado. Validador de entorno ejecutado con datos sintéticos: caso válido y rechazos. Reproducción del harness documentada. | Clone falló por proxy; Docker cloud permission denied. Sin checkout completo ni E2E. Prueba actual llega a checkout, no completa suscripción; siguiente cambio técnico propuesto en payment-ui-runtime y reentrada. |
| Organización | Sergio·Hoy actualizado y releído: resultados y tres acciones personales. Conserva 20 IDs y 35 borradores. | No Calendar nuevo, precio, ingresos o publicación declarados. |

## Evidencia recuperable

- [Workshop y hojas](https://chatgpt.com/space/page_d5d8f16b59d481919b0b597e4d25d5b4), secuencia 6: guía reservada y dos hojas sin soluciones.
- [W1 corregida](https://chatgpt.com/space/page_52ea218e0d2081918382021b71d8e8a0), sección Entrega corregida vigente. JSON válido SHA 219f39389dc68586362173895e066e328773b82646c02d012f11f08bb03edc8a.
- [n8n](https://chatgpt.com/space/page_d43d9736e728819191c34648bd68dc75), TANDA-01-CLAIM e Identificación de PostgreSQL. No se leyeron valores de credenciales ni se consultaron datos de producto.
- [Video y diagnóstico](https://chatgpt.com/space/page_3559f542705c8191b44d8d31326e6de4); diagnóstico adicional en Page W1, sección DIAG-HYPERFRAMES.
- [Producto](https://chatgpt.com/space/page_160800c9076881919764ae7971519b43), secuencia 2, reproducción y límites.
- [Exportación Jefe](https://chatgpt.com/space/page_a91f59f36d4c81918b61447696c651a2), secuencia 2; JSON SHA a2417d1e31a3b03a8e7ed5551bd9d22be7e76a6da010605ea11d9399584451d9, conjunto SHA 298691eb3dd55d2115199ee196c96668d9b85923b4353c5b82be6842debf36ab.
- [Sergio·Hoy](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964).

## Corrección de coordinación y decisión técnica

Sergio cuestionó afirmar que los frentes seguían avanzando cuando varios habían cerrado bloqueados. Se corrige: entrega documental, ejecución de un componente e integración completa son estados diferentes. Se detuvieron nuevos encargos de producción contra esas condiciones. La prueba de W1 y el workshop no acreditan video, producto o mensajería integral.

Por petición explícita de Sergio se inspeccionó y detuvo Linux local conservando datos. Docker apuntaba al named pipe local dockerDesktopLinuxEngine. Se pararon ordenadamente 11 contenedores fiscal-mock, Docker Desktop y Ubuntu/WSL; ambas distribuciones quedaron Stopped, sin proceso vmmemWSL. No se borraron imágenes/volúmenes/distribuciones, no se cerraron apps de usuario ni se modificó el VPS. Para retomar esos proyectos se deberán iniciar sus servicios de forma consciente.

Equipo observado: i5-11400H, 12 procesadores lógicos, 23,6 GiB RAM utilizable. Primera lectura 80% en uso/4,7 GiB libres; lectura inmediatamente previa a parada 8,7 GiB y posterior 10,6 GiB. Las lecturas son instantáneas, no atribuir toda variación a nuestra acción ni prometer capacidad por RAM total.

Node 24.13.0 creó su hijo correctamente en Windows. HyperFrames 0.9.9 existente pasó check con una advertencia de estructura y sin audio. Render técnico local de 6 s con --low-memory-mode, un trabajador: H.264, 1080×1920, 24 fps, 144 fotogramas, 124644 bytes; motor 17,1 s, comando 20,9 s. FFmpeg decodificó todo; tres fotogramas inspeccionados. SHA c7701e96626f704baf822d3da90d8ce1a041ec36f8a7737a45fcc60b7abdc039. MP4 subido a la Page de Video. Al terminar había 10,6 GiB libres; no se midió pico. No es D1, pieza comercial ni prueba de audio.

La caché NPM aislada no tenía el CLI (ENOTCACHED); el acceso aprobado a caché Windows permitió usar la versión fijada sin actualizar paquetes. No se alteraron sandbox, TLS o proxy. Esta prueba acredita una ruta local concreta; no garantiza todas las tareas ni soluciona el EPERM cloud.

## Primera unidad de trabajo recomendada

Cerrar una pieza completa antes de multiplicar sesiones: material de referente accesible y análisis audiovisual con cobertura explícita → idea/guion con historia, enseñanza, demostración y cierre → lista exacta de tomas de Sergio → edición/render con recursos acotados → revisión y publicación sólo con autorización aplicable. Comenzar por una muestra, conservando el catálogo de referentes pendiente: Hormozi/Gadzhi/Heras para oferta y relato; Pedro para edición. No afirmar análisis integral donde sólo hay fotogramas o clasificadores de audio.

Local se recomienda para la prueba de edición que hoy sí ejecuta; cloud conserva servicios y trabajo demostrado. No se migraron chats ni se adoptó una nueva arquitectura total. Git sigue como fuente oficial, Notion como vista cotidiana. n8n requiere acceso administrativo seguro para verificar/provisionar base/rol separado; no trasladar esa búsqueda al usuario ni instalar un servicio pesado en el VPS por defecto.

[OpenAI Docs: entornos](https://learn.chatgpt.com/docs/environments/modes) distingue ejecución local y cloud con archivos propios. [Cloud](https://learn.chatgpt.com/docs/environments/cloud-environments) documenta continuidad con PC dormida; no acredita que nuestro circuito entero funcione. La recomendación de reparto se apoya además en estas pruebas, no sólo en la documentación.
