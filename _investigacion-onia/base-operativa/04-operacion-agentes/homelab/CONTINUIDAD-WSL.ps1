$ErrorActionPreference = 'Stop'
if ($env:COMPUTERNAME -ne 'DESKTOP-0GGGNMF') { throw 'Solo DESKTOP-0GGGNMF' }
$oniaTaskName = 'OnIA-Ubuntu-Continuidad'
if (Get-ScheduledTask -TaskName $oniaTaskName -ErrorAction SilentlyContinue) {
    throw 'La tarea ya existe: conservarla y consultar su estado; no sobrescribir'
}
$oniaUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$oniaPowerShell = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
$oniaAction = New-ScheduledTaskAction -Execute $oniaPowerShell -Argument '-NoProfile -NonInteractive -WindowStyle Hidden -Command "& $env:SystemRoot\System32\wsl.exe --distribution Ubuntu --user onia-worker --exec /usr/bin/sleep infinity; exit $LASTEXITCODE"'
$oniaTrigger = New-ScheduledTaskTrigger -AtLogOn -User $oniaUser
$oniaPrincipal = New-ScheduledTaskPrincipal -UserId $oniaUser -LogonType Interactive -RunLevel Limited
$oniaSettings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit ([TimeSpan]::Zero) -MultipleInstances IgnoreNew -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1) -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$oniaTask = New-ScheduledTask -Action $oniaAction -Trigger $oniaTrigger -Principal $oniaPrincipal -Settings $oniaSettings -Description 'Mantiene Ubuntu activo durante la sesion Windows para el worker OnIA. No cambia suspension ni seguridad.'
Register-ScheduledTask -TaskName $oniaTaskName -InputObject $oniaTask | Out-Null
Start-ScheduledTask -TaskName $oniaTaskName
Start-Sleep -Seconds 5
Get-ScheduledTask -TaskName $oniaTaskName | Select-Object TaskName, State
