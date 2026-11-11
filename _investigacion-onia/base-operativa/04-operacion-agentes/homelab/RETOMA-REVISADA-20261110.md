# Retoma revisada de onia-worker — 10 noviembre 2026

> Siguiente paso del corte PE: [diagnóstico y retoma v3](RETOMA-PE-20261111.md). Primero diagnóstico; no repetir v2 ni dar la PC por conectada.

> **Este intento ya se ejecutó y volvió a detenerse.** Consultar [ALTA-DETENIDA-v2-20261110.md](ALTA-DETENIDA-v2-20261110.md). No repetir este comando sobre los archivos creados por ese intento; requiere diagnóstico y otra retoma revisada.

Corrección del corte documentado en [ALTA-DETENIDA](ALTA-DETENIDA-20261110.md). Sólo DESKTOP-0GGGNMF/Ubuntu WSL2. No aplicada por Codex al escribir este informe.

Instalador nuevo SHA256: `0521e2f4286f50734e0c2c01be09d05abb0393edd74bf6a5196ec3ecd98fe871`. Conserva el original y descargá esta versión con otro nombre, `alta-onia-worker-v2.py`. No usar el hash anterior.

La consulta local exige la frase exacta de denegación para el usuario y hostname con salida0 o1; no basta código0 ni coincidencia parcial. Se conserva el aislamiento, sandbox, huella y orden de publicación de la llave. La retoma es explícita y sólo admite el corte observado: UID/GID1001, grupo exclusivo sin alias ni otros usuarios, shell nologin, password bloqueado con asterisco, home esperado y ninguna ruta de instalación existente. Exige sudo ejecutable y respaldo previo privado de root sin el worker. No borra ni recrea la cuenta y no salta pruebas.

## Paso de Boss/Sergio en la PC autorizada

Conservar todos los archivos anteriores. Tras descargar el instalador nuevo como `Downloads/alta-onia-worker-v2.py`, ejecutar en PowerShell de la PC de casa:

```powershell
$oniaSetupV2 = Join-Path $env:USERPROFILE 'Downloads\alta-onia-worker-v2.py'
if ((Get-FileHash -Algorithm SHA256 $oniaSetupV2).Hash.ToLower() -ne '0521e2f4286f50734e0c2c01be09d05abb0393edd74bf6a5196ec3ecd98fe871') { throw 'El archivo no coincide con el revisado' }
$oniaLinuxV2 = (wsl.exe -d Ubuntu -- wslpath -u $oniaSetupV2).Trim()
if ($LASTEXITCODE -ne 0) { throw 'No se pudo localizar el archivo en Ubuntu' }
wsl.exe -d Ubuntu -u root -- python3 $oniaLinuxV2 --apply --resume-backup /root/onia-worker-originales-20261110T173148Z
```

Ese respaldo es el ORIGINAL reportado por Boss. No sustituirlo por el nuevo respaldo que ya contendrá la cuenta. Si el estado cambió o la salida es ALTA DETENIDA, conservar y diagnosticar sin repetir a ciegas.

Después de alta_local OK: seguir el preflight de loopback y de Tailscale Serve en [ALTA-ONIA-WORKER](ALTA-ONIA-WORKER.md), preservando forwards existentes. Codex contrasta la huella antes de autenticar y prueba aislamiento remoto; WSL persistente requiere comprobación separada. No afirmar homelab aceptado sólo por ejecutar este script.

## Evidencia de revisión y pruebas

Revisor distinto `/root/revision_puente_boss`, solicitado Sol6.1 high (modelo efectivo/cuota no visibles): inicialmente cambios por grupo compartido y ausencia de sudo; corregidos y dictamen bueno para retoma. No se abrió sesión de la PC desde Codex. Suite12:11correctas y1integración bwrap omitida en sandbox; el wrapper de aislamiento no cambió frente a master. La prueba real de WSL está pendiente.

La observación de sudo-rs procede del recibo de Boss en esta PC, no de asumir que cualquier sudo con código0 deniega. Fuente técnica: [proyecto sudo-rs](https://github.com/trifectatechfoundation/sudo-rs). No se ejecutó sudo en el VPS.
