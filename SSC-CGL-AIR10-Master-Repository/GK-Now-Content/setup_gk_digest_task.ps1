<#
================================================================================
 setup_gk_digest_task.ps1
 Registers a Windows Scheduled Task that runs the daily GK Current-Affairs
 digest (gknow.in) once every day (default 07:15). Runs only when the PC is on;
 if it was off at the scheduled time, it catches up at next logon/startup
 (StartWhenAvailable). The script itself commits + pushes the rebuilt PDF.

 USAGE (no admin needed for a per-user task):
   Right-click -> "Run with PowerShell"
   OR from a PowerShell window:
       powershell -ExecutionPolicy Bypass -File .\setup_gk_digest_task.ps1
   Optional custom time:
       powershell -ExecutionPolicy Bypass -File .\setup_gk_digest_task.ps1 -Time "06:45"

 To remove later:
   Unregister-ScheduledTask -TaskName "DailyGKDigest" -Confirm:$false
================================================================================
#>

param(
    [string]$Time = "07:15",
    [string]$TaskName = "DailyGKDigest"
)

$ErrorActionPreference = "Stop"

# Resolve paths relative to this script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$Bat = Join-Path $ScriptDir "run_gk_digest.bat"

if (-not (Test-Path $Bat)) {
    Write-Error "Cannot find run_gk_digest.bat next to this script at: $Bat"
    exit 1
}

Write-Host "Setting up daily task '$TaskName' at $Time ..." -ForegroundColor Cyan
Write-Host "  Script folder: $ScriptDir"
Write-Host "  Launcher     : $Bat"

# Remove any existing task with the same name (idempotent re-install)
$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "  Removing existing task with same name..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Action: run the batch launcher in its own folder
$Action = New-ScheduledTaskAction -Execute $Bat -WorkingDirectory $ScriptDir

# Trigger: every day at the chosen time
$Trigger = New-ScheduledTaskTrigger -Daily -At $Time

# Settings: catch up missed runs, run on battery, don't stop if it runs long
$Settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
    -RestartCount 2 `
    -RestartInterval (New-TimeSpan -Minutes 5)

# Run as the current user, only when logged on (no password needed)
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Description "Scrapes gknow.in 8 CA categories daily -> one combined GK digest PDF, auto-pushed." | Out-Null

Write-Host ""
Write-Host "Done. Task '$TaskName' is scheduled daily at $Time." -ForegroundColor Green
Write-Host ""
Write-Host "Test it now (runs immediately):" -ForegroundColor Cyan
Write-Host "    Start-ScheduledTask -TaskName `"$TaskName`""
Write-Host ""
Write-Host "Check status:" -ForegroundColor Cyan
Write-Host "    Get-ScheduledTaskInfo -TaskName `"$TaskName`""
Write-Host ""
Write-Host "Remove it later:" -ForegroundColor Cyan
Write-Host "    Unregister-ScheduledTask -TaskName `"$TaskName`" -Confirm:`$false"
