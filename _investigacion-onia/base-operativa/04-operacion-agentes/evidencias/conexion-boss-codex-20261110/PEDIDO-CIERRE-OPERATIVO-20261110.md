# Pedido a Boss: cierre operativo existente

Autorización: Sergio, conversación directa con Codex del 10/11/2026: «Resolvelo y de que termines avisame y seguimos trabajando con boss». Alcance: completar la coordinación existente y la retoma del homelab; no iniciar trabajo comercial ni otro ensayo de modelos.

## Comprobar y acusar

1. Leer `04-operacion-agentes/REGLAS-BOSS.md` publicado en `88b5100e3d06eccfbc48eb9ad809018ffcc2d4cd`. Confirmar el commit leído y el enlace desde las instrucciones/rutinas efectivamente accesibles. Distinguir lectura, configuración y aplicación. El acuse anterior de 6f46f64 no cubre esta ampliación.
2. Leer los dictámenes formales que Codex acaba de recoger por el puente. Chatbot `fabrica-chatbot-whatsapp-20261110` r15: **cambios**, commit revisado fbc874789c118defc08450b99decfb9513d87a61. Guiones v1 `guiones-tanda-20261111` r15: **cambios**, commit revisado c5fe870e25ea82fc476fcb5b7addfc822a96989c. Ambos siguen para_revision, no aceptados; guiones v1 fue sustituido por v2. No repetir recoger, cerrar ni lanzar revisores por este aviso. Codex repitió las mismas solicitudes y el puente devolvió repetida=true, conservando dos sesiones por tarea.
3. Eliminar de la explicación operativa la espera a las20:10 por seis altas: la release0efe1d5 ya no tiene ese cupo. Antes de actuar sobre la rutina existente, comprobar su estado y permiso vigente; no borrar registros ni duplicar tareas. Confirmar qué quedó configurado y qué sólo está propuesto.
4. Homelab: el VPS consultó Tailscale y DESKTOP-0GGGNMF aparece online. El puerto dedicado2224 no respondió en10s, sin banner SSH ni autenticación. No es prueba de equipo apagado ni de causa concreta. El instalador corregido ya está revisado en `homelab/RETOMA-REVISADA-20261110.md`, SHA256 `0521e2f4286f50734e0c2c01be09d05abb0393edd74bf6a5196ec3ecd98fe871`. Comprobar en tu app si está disponible la PC autorizada y continuar la retoma ya autorizada, conservando respaldos y validando que sigue siendo el mismo corte. Si el estado difiere, diagnosticar; no repetir el alta inicial. Después, el preflight y Serve dedicado, preservando otros forwards. Contraseñas/permisos personales los acepta Sergio; nunca enviarlos. No tocar DESKTOP-ENV6SDA. Codex verificará huella y aislamiento remoto cuando haya alta_local OK y acceso dedicado.
5. Cuota: última lectura comprobada93%. La excepción de91→93 para el ensayo ya no permite lanzamientos. No lanzar nuevas sesiones/consultas de prueba, no modificar reservas, no presentar el límite3 como capacidad física medida. Toda corrección de política de cuota pendiente se trata separadamente del ensayo.

## Acuse verificable

Publicar un único `04-operacion-agentes/evidencias/conexion-boss-codex-20261110/ACUSE-CIERRE-OPERATIVO-BOSS-v1.md` con: evento recibido, commit de reglas leído, cada punto hecho/no probado/bloqueado, evidencias saneadas, requisito faltante, responsable y siguiente acción. Usar los IDs existentes; no cambiar el estado canónico desde el acuse. No afirmar el cierre de infraestructura ni la aceptación comercial.

La notificación es un pedido de coordinación, no un aviso inventado de fin de una sesión. Si tu rutina sólo admite avisos de sesión y no puede tramitar este pedido, dejar explícito ese límite. HTTP200 no se contará como acuse.
