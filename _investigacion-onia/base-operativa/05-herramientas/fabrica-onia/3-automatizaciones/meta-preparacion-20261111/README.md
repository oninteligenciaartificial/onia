# Preflight de conexión IG/FB para NEGOCIO

Entrega local del encargo `meta-preparacion-canales-20261111`, 12-nov-2026 UTC. Ninguna de las cuatro rutas está lista para conexión real. Se reutiliza [el adaptador existente](../meta-canales-20261111/README.md) sin modificarlo, sin duplicar motor ni crear un workflow. Este documento y su JSON de evidencia no sustituyen el registro canónico del harness.

Disponibles: normalización sintética, firma/challenge, motor determinista, persistencia SQLite, idempotencia, cese y outbox simulada. Faltan cuentas/permisos actuales comprobados, política/versiones verificadas, transporte real, receptor HTTPS revisado, credencial compatible en n8n, aprobación de textos y ensayo real por ruta. `RealConnector` rechaza siempre; habilitar envíos en config también se rechaza. La oferta aún tiene aprobación editorial falsa.

## Reproducir

Desde la raíz del checkout, Python 3.10+ y biblioteca estándar, sin instalación:

```bash
P=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/3-automatizaciones/meta-preparacion-20261111
M=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/3-automatizaciones/meta-canales-20261111
python3 -B "$P/preflight.py"
python3 -B "$P/preflight.py" --ensayo
python3 -B -m unittest discover -s "$M" -p 'test_*.py' -v
```

Sin argumentos, el preflight sólo lee fuentes locales y escribe JSON por stdout. No descubre ni imprime variables de entorno o secretos. `--ensayo` ejecuta **el ensayo existente** en un hijo Python aislado, con sockets bloqueados y sin bytecode; éste usa y retira DB temporales privadas fuera del repo. No inicia servicios. El script no guarda archivos: el operador puede redirigir stdout a una ruta propia. Código 0 significa contrato/ensayo local correcto; **no significa acceso o canal listo**. Fuentes faltantes/corruptas provocan fallo, nunca aprobación. `listo_para_conectar` y `e2e_real` permanecen falsos. La consulta oficial se conserva aparte; el script no hace red ni actualiza sus resultados.

Resultado actual en [evidencia/preflight.json](evidencia/preflight.json): cuatro recorridos, 16 combinaciones de transporte ficticio, cero envíos reales, hashes de oferta coincidentes y fuentes intactas. [evidencia/pruebas.txt](evidencia/pruebas.txt): 44/44 pruebas, sin omisiones. El reloj del ensayo es fijo (`2026-11-11T21:00:00Z`); no acredita vigencia comercial hoy. No se rehashearon evidencias anteriores.

## Cuatro rutas: contrato y dependencia real

| Ruta | Contrato local disponible | Cuenta/requisito por confirmar | Dependencia real y ensayo pendiente |
|---|---|---|---|
| IG comentario | `object=instagram`, `changes.field=comments`; ID `value.id`, actor `from.id`, origen `media.id`; intención `private_reply` | Cuenta profesional propia, contenido elegible, modalidad Instagram Login de la app existente, suscripción de comentarios autorizada | Elegibilidad de respuesta privada y timestamp de creación verificable. `entry.time` del fixture no acredita edad del comentario. Ensayo: NEGOCIO en contenido propio → una respuesta privada recibida; replay/reinicio sin segunda salida, baja. No presupone apertura de DM. |
| IG DM | `entry.messaging`, `message.mid/text`, sender/recipient, timestamp ms; intención `dm` | Misma cuenta/login, recepción de mensajes por app y autorización correspondiente | DM entrante elegible, identidad y ventana comprobadas. Puede ensayarse directamente sin comentario previo. NEGOCIO → información; DM posterior WHATSAPP → enlace con contexto; BAJA cancela. Para recorrido desde comentario, comprobar identidad/origen dentro de esa red. |
| FB comentario | `object=page`, `changes.field=feed`, `item=comment`, `verb=add`; `comment_id/post_id/created_time` | Página propia autorizada, tareas del titular, token de Página y suscripción feed aplicables | Permisos y modalidad/endpoint de respuesta privada propios de FB. Ensayo de comentario NEGOCIO → respuesta privada elegible, replay/reinicio y BAJA. Ediciones/borrados no disparan venta. No necesita una cuenta IG. |
| FB DM | `object=page`, `entry.messaging`, `mid`, sender/recipient; intención `dm` | Página y Messenger, identidad PSID y token/tareas autorizados | Mensaje entrante a la Página y política aplicable. Ensayo independiente de comentario: información → WHATSAPP en DM posterior → enlace aprobado → BAJA. No fusionar PSID con Instagram o WhatsApp. |

En todas: sobres reales saneados aún ausentes; firma SHA256 y challenge sólo probados sintéticamente. Revalidar límites de cuerpo, unidad/origen de fechas, ecos, adjuntos y cuenta receptora contra captura autorizada antes de adaptar fixtures. Las pruebas existentes cubren entrada inválida, colisión de ID, duplicados, reinicio, concurrencia, baja compartida comentario/DM, oferta vencida/cambiada y fallos simulados. Éxito simulado, rechazo, timeout e incierto son terminales: no equivalen a mensajes enviados.

## Credenciales, permisos y versiones

[accesos.md](../../../accesos.md) conserva evidencia previa: app **OnIA Social API**, Instagram Login seleccionado para el piloto propio; `META_IG_ACCESS_TOKEN` sin acceso comprobado. No usar la app/token Ads como sustituto. Es evidencia histórica de coordinación, no inspección de cuentas en esta sesión. Facebook necesita su propia Página/token/tareas comprobados; no hay evidencia actual de éstos. Instagram Login no se debe condicionar por analogía a una Página FB; si se cambia a Facebook Login o Unified Login, revisar de nuevo contrato, relación de activos, scopes y hosts. No se cambia modalidad aquí.

| Ruta | Candidatos históricos que hay que contrastar; no son permisos concedidos | Bloqueo actual |
|---|---|---|
| IG comentario / Instagram Login | `instagram_business_basic`, `instagram_business_manage_comments`; comprobar requisitos de private reply, incluido permiso de mensajes si corresponde | Scopes finales, nivel de acceso, revisión, modo de app, requisitos de verificación, token/tipo/vencimiento y endpoint exacto desconocidos |
| IG DM / Instagram Login | `instagram_business_basic`, `instagram_business_manage_messages` | Mismos bloqueos; recepción por la app y ventana por verificar |
| FB comentario | `pages_manage_metadata`, `pages_read_engagement`, `pages_read_user_content`, `pages_messaging`, según operación documentada | Token/tareas/suscripción feed, permisos finales y endpoint de private reply desconocidos |
| FB DM | `pages_messaging`, `pages_manage_metadata`, según documentación vigente | Token/tareas, recepción, revisión y ventana desconocidos |

No se propone respuesta pública; no añadir `pages_manage_engagement` por analogía. No mezclar prefijos `instagram_business_*` con los de Facebook Login. No fijar ninguna ventana numérica de Meta a partir del reloj local: una hora de caducidad y cinco minutos de tolerancia futura son controles del ensayo. Versión Graph vigente, retiro de versiones, cuotas y elegibilidad no verificables hoy. La referencia antigua v2.6 no sirve como versión candidata.

n8n: ningún MCP específico disponible en el catálogo de esta sesión. No se leyó API ni secretos. `accesos.md` registra una preparación histórica 2.43.7 y un piloto sintético, sin acreditar versión instalada actual o conexión Meta. Los dos JSON WhatsApp existentes están inactivos en disco; no acreditan estado remoto ni compatibilidad. Antes de conexión, Operaciones deberá cotejar versión real, esquema de nodos/credenciales, export anterior y callback. No reinstalar ni cambiar proxy/base/cifrado. Credenciales de ejecución quedan en Credentials de n8n, sólo referencias en exportaciones. No se prepara otra copia de esos workflows en esta entrega.

## Fuentes y límites de consulta

[fuentes-oficiales.json](fuentes-oficiales.json) registra los intentos de lectura del 12-nov-2026 UTC. Las páginas de Meta devolvieron 429, inaccesibilidad sin status o cache miss; Postman sólo mostró contenedor visual. La búsqueda indexó un fragmento de la colección oficial de Meta para mensajes IG, pero no permitió leer sus condiciones completas: no se usa para afirmar ventanas o permisos suficientes. Resultados de terceros descartados como prueba normativa. No hay API real de Meta/n8n invocada ni inspección privada de cuentas en esta sesión.

Se reutilizaron [MATRIZ-META](../meta-canales-20261111/MATRIZ-META.md), [contrato](../meta-canales-20261111/contrato-canales.json), [plan de prueba real](../meta-canales-20261111/ACTIVACION-PENDIENTE.md), [PRUEBAS](../meta-canales-20261111/PRUEBAS.md), código/fixtures y oferta compartida. Su estado textual histórico `para_revision` no certifica la aceptación actual del harness. La sesión recibe el adaptador como reutilizable por el encargo; no modifica ni reconstruye el registro canónico.

## Orden de conexión seguro (pendiente; no ejecutado)

1. **WhatsApp primero e independiente.** Continuar su ensayo autorizado con su propio adaptador y operador; IG/FB no son precondiciones. Este preflight no ejecuta ni declara superado ese ensayo. Configurar derivación IG/FB sólo después de comprobar el destino propio y el ensayo WhatsApp. Pago/acceso/soporte conservan sus comprobaciones separadas.
2. En paralelo, Sergio/Operaciones recuperan documentación oficial legible y cotejan privadamente cuentas/login, permisos concedidos, revisión/nivel de acceso, tokens y vencimiento, versiones soportadas, ventanas, endpoints y suscripciones para cada ruta. Cierre: recibo saneado por canal sin desconocidos relevantes. Si una ruta sigue bloqueada, las otras avanzan independientemente.
3. Desarrollador, con encargo y rutas propios, concilia sobres reales autorizados, implementa receptor/transporte que hoy faltan y obtiene revisión independiente. Contenido/Sergio aprueban oferta/textos vigentes. Operaciones prepara referencias de credenciales y persistencia fuera del repo; export/respaldo anterior antes de cualquier cambio autorizado en n8n. Sin eso no existe conexión ejecutable.
4. Probar primero DM entrante de cada red que cumpla sus requisitos, luego comentario → respuesta privada de esa misma red. DM directo no depende de comentario, ni Facebook de Instagram. Cada ensayo requiere sí aplicable de Sergio, cuenta controlada, contenido propio elegible, texto exacto, límite de respuestas, franja, operador y coste cero comprobado. Es una secuencia sugerida, no una autorización nueva.
5. Con WhatsApp ya ensayado y destino aprobado, un DM posterior WHATSAPP con contexto prepara el enlace `wa.me` desde configuración privada. La persona lo abre e inicia WhatsApp voluntariamente. Conservar referencia opaca/origen; no unir identidades entre redes por inferencia ni transferir contactos. Confirmar recepción y correlación autorizada, no sólo HTTP 200.
6. Antes de activación comercial por canal, revisar evidencia real: recepción, una sola salida tras replay/reinicio, baja y ausencia de reintento incierto. Mantener clave persistente derivada de canal/cuenta/ID de evento, detectar colisiones de payload y separar DB/outbox de simulación y producción. La DB temporal del ensayo no se migra a producción. Ante timeout, conciliar resultado remoto por mecanismo documentado antes de cualquier nueva escritura. No vaciar deduplicación para repetir. Revalidar oferta también al consumir pendientes.

Parada: ante baja, identidad/firma inválida, política desconocida, oferta no vigente, coste o transporte incierto, impedir nuevas salidas y conservar evidencia privada. Desactivación/rollback futuro sólo bajo permiso aplicable, con export previo y sin borrar IDs/deduplicación. En esta entrega basta dejar de ejecutar comandos: no hay servicio ni cambio remoto que revertir.

Responsables de brechas: Sergio/Operaciones (cuentas, documentación, destino y ensayo limitado), Contenido/Sergio (textos), desarrollador/revisor distintos (receptor/transporte y compatibilidad n8n), coordinadora (cerrar, revisión del commit publicado e integración si corresponde). Ninguna de esas dependencias externas se presenta como resuelta.
