# D1 · procedencia y dependencias externas

Esta es una copia textual del piloto privado ya ejecutado, **no un paquete portable probado**. No se ejecutaron el render ni el verificador durante la consolidación. Código, configuración y JSON se conservan byte a byte; los logs check/render omiten únicamente progreso y trazas repetitivas, con hash original y transformación en [procedencia.json](procedencia.json). El reporte indica dónde hubo muestreo visual, sin atribuir escucha.

Origen local: `C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/piloto-d1-local/`. `run.mjs` conserva su ruta concreta de caché HyperFrames y Chrome; no se adaptó a otro equipo. `verificar.py` depende de FFmpeg/ffprobe y Pillow; no se verificaron sus versiones ni disponibilidad para una ejecución nueva. Node 24.13.0 y Python 3.12.10 fueron observados por Desarrollo en la revisión local, no instalados aquí.

| Dependencia o medio fuera de Git | Versión/hash y ubicación |
|---|---|
| HyperFrames | 0.9.9; ruta original `C:/Users/PC/AppData/Local/npm-cache/_npx/020dad40ade292f2/node_modules/hyperframes`; integridad completa de instalación no revalidada. |
| Chrome | Ruta original `C:/Program Files/Google/Chrome/Application/chrome.exe`; versión no comprobada en esta consolidación. |
| GSAP | 3.15.0; `assets/gsap-3.15.0.min.js` bajo el origen local. SHA-256 `92bb9a96476f983d212a2bc4f54c889039c1696dd4461d40a736860938570fbb`. No se copió la dependencia. |
| Tipografía regular | `assets/segoeui.ttf`; SHA-256 `704eada12961a27fd271f7d3b09e2066520e758390c1776744eff430fee30f6e`. |
| Tipografía semibold | `assets/segoeuisb.ttf`; SHA-256 `6c3fd894b19950b10c34bf64069ef821eaf2f58f959146306fee5b367472e501`. |
| Tipografía bold | `assets/segoeuib.ttf`; SHA-256 `b169e636719880976a97e94e3b1cb3dbe5f4a38eabc037bf9f2a9165154c3ad2`. |
| MP4 | `d1-piloto-silencioso.mp4`; SHA-256 `c41798b0c33c1d42232aba8a542696748b548b1ba327560d3ff148edc5f1c71c`, 385.060 bytes, 43 s y cero audio. Hash cotejado localmente. |
| Muestras visuales | `contacto-visual.jpg` y `fotogramas/` bajo el origen local; tiempos en [verificacion.json](verificacion.json). No se copiaron JPG/PNG. |

Los hashes de dependencias/tipografías proceden del [registro original](sha256.json); no equivalen a aprobación de redistribución. Tipografías, MP4, imágenes, dependencias y `.work` quedan fuera de este paquete. La revisión de una copia futura exige recuperar los recursos por su vía autorizada y comprobar las rutas antes de ejecutar. Esta nota no autoriza instalación, render o publicación.
