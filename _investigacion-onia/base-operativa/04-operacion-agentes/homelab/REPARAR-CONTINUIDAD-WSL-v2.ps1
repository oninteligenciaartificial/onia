$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSEdition -ne 'Desktop' -or $PSVersionTable.PSVersion.Major -ne 5 -or -not [Environment]::Is64BitProcess) { throw 'Usar Windows PowerShell 5.1 de 64 bits' }
if ($env:COMPUTERNAME -ne 'DESKTOP-0GGGNMF') { throw 'Solo la PC de casa autorizada' }
$oniaName = 'OnIA-Ubuntu-Continuidad'
$oniaTask = Get-ScheduledTask -TaskName $oniaName
if ($oniaTask.State -eq 'Running') { throw 'La tarea esta corriendo: no sustituir durante trabajos' }
if ($oniaTask.Principal.LogonType -ne 'Interactive' -or $oniaTask.Principal.RunLevel -ne 'Limited') { throw 'Principal inesperado: detenerse' }
if ($oniaTask.Actions.Count -ne 1 -or $oniaTask.Actions[0].Execute -notlike '*\WindowsPowerShell\v1.0\powershell.exe' -or $oniaTask.Actions[0].Arguments -ne '-NoProfile -NonInteractive -WindowStyle Hidden -Command "& $env:SystemRoot\System32\wsl.exe --distribution Ubuntu --user onia-worker --exec /usr/bin/sleep infinity; exit $LASTEXITCODE"') { throw 'Accion distinta de v1: conservar y revisar' }
$oniaDir = Join-Path $env:LOCALAPPDATA ('OnIA\WSLContinuidad\v2-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $oniaDir | Out-Null
Export-ScheduledTask -TaskName $oniaName | Set-Content -LiteralPath (Join-Path $oniaDir 'tarea-anterior.xml') -Encoding Unicode
$oniaExe = Join-Path $oniaDir 'OnIA-WSL.exe'
$oniaSource = @'
using System;
using System.Diagnostics;
using System.IO;
public static class OniaWslContinuidad {
    [STAThread]
    public static int Main() {
        if (!String.Equals(Environment.MachineName, "DESKTOP-0GGGNMF", StringComparison.OrdinalIgnoreCase)) return 10;
        string dir = AppDomain.CurrentDomain.BaseDirectory;
        try {
            var info = new ProcessStartInfo();
            info.FileName = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Windows), "System32", "wsl.exe");
            info.Arguments = "--distribution Ubuntu --user onia-worker --exec /usr/bin/sleep infinity";
            info.UseShellExecute = false;
            info.CreateNoWindow = true;
            info.WindowStyle = ProcessWindowStyle.Hidden;
            File.AppendAllText(Path.Combine(dir, "estado.log"), DateTime.UtcNow.ToString("o") + " inicio\r\n");
            using (var p = Process.Start(info)) {
                p.WaitForExit();
                File.AppendAllText(Path.Combine(dir, "estado.log"), DateTime.UtcNow.ToString("o") + " salida=" + p.ExitCode + "\r\n");
                return p.ExitCode;
            }
        } catch (Exception e) {
            File.AppendAllText(Path.Combine(dir, "estado.log"), DateTime.UtcNow.ToString("o") + " error=" + e.GetType().Name + "\r\n");
            return 11;
        }
    }
}
'@
Add-Type -TypeDefinition $oniaSource -Language CSharp -OutputAssembly $oniaExe -OutputType WindowsApplication
if (-not (Test-Path -LiteralPath $oniaExe -PathType Leaf)) { throw 'No se genero el lanzador: tarea sin modificar' }
$oniaCurrent = Get-ScheduledTask -TaskName $oniaName
if ($oniaCurrent.State -eq 'Running' -or (Export-ScheduledTask -TaskName $oniaName).TrimEnd() -ne (Get-Content -LiteralPath (Join-Path $oniaDir 'tarea-anterior.xml') -Raw).TrimEnd()) { throw 'La tarea cambio durante la preparacion: conservar archivos y revisar' }
$oniaAction = New-ScheduledTaskAction -Execute $oniaExe
Set-ScheduledTask -TaskName $oniaName -Action $oniaAction | Out-Null
Start-ScheduledTask -TaskName $oniaName
Start-Sleep -Seconds 10
Get-ScheduledTask -TaskName $oniaName | Select-Object TaskName, State
Get-ScheduledTaskInfo -TaskName $oniaName | Select-Object LastRunTime, LastTaskResult
Write-Output ('Respaldo y registro privados: ' + $oniaDir)
