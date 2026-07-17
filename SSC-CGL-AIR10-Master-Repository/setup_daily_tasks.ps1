<#
================================================================================
 setup_daily_tasks.ps1   (repo root)
 Registers ALL daily study tasks in one go:
   1. DailyEditorialVocabulary   07:00  -> Daily-Editorial-Vocabulary\run_daily_vocab.bat
   2. DailyOneWordSubstitution   07:05  -> One-Word-Substitution\run_ows.bat
   3. DailyGKCurrentAffairs      07:10  -> GK-Now-Content\run_gk.bat
   4. DailyBookReleases          07:15  -> Static-GK\run_books.bat
   5. DailyCurrentAffairsDigest  07:20  -> GK-Now-Content\run_ca_digest.bat
   6. DailySummitsEvents         07:25  -> Static-GK\run_summits_events.bat
   7. DailyPoliticalReforms      07:30  -> Static-GK\run_political_reforms.bat
   8. DailyCommitPush            07:45  -> run_commit_push.bat  (end-of-day sweep: commit ALL + push)

 Times are staggered so they don't all fire at once. Each task:
   - runs once a day, only when the PC is on,
   - catches up missed runs at next logon (StartWhenAvailable),
   - runs as the current user, no admin / password needed.

 USAGE (no admin needed for per-user tasks):
   Right-click -> "Run with PowerShell"
   OR:  powershell -ExecutionPolicy Bypass -File .\setup_daily_tasks.ps1
   Custom base time (first task; others +5/+10 min):
        powershell -ExecutionPolicy Bypass -File .\setup_daily_tasks.ps1 -BaseTime "06:30"

 Remove all later:
   powershell -ExecutionPolicy Bypass -File .\setup_daily_tasks.ps1 -Remove
================================================================================
#>

param(
    [string]$BaseTime = "07:00",
    [switch]$Remove
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Task name -> launcher .bat (relative to repo root) and minute offset from BaseTime
$Tasks = @(
    @{ Name = "DailyEditorialVocabulary"; Bat = "Daily-Editorial-Vocabulary\run_daily_vocab.bat"; Offset = 0;  Desc = "Daily SSC/UPSC editorial vocabulary (HTML, highlights today's words)." },
    @{ Name = "DailyOneWordSubstitution"; Bat = "One-Word-Substitution\run_ows.bat";              Offset = 5;  Desc = "Daily One-Word Substitution builder (HTML, highlights today's words)." },
    @{ Name = "DailyGKCurrentAffairs";    Bat = "GK-Now-Content\run_gk.bat";                      Offset = 10; Desc = "Daily GK / Current Affairs mined from GKToday (HTML, highlights today's)." },
    @{ Name = "DailyBookReleases";        Bat = "Static-GK\run_books.bat";                       Offset = 15; Desc = "Daily book-release headlines from GKToday into Books-and-Authors.html." },
    @{ Name = "DailyCurrentAffairsDigest"; Bat = "GK-Now-Content\run_ca_digest.bat";             Offset = 20; Desc = "Daily Current Affairs digest (Sports/Days/Summits/Agreements/Awards, dated PDF) - auto commits & pushes to git." },
    @{ Name = "DailySummitsEvents";        Bat = "Static-GK\run_summits_events.bat";            Offset = 25; Desc = "2-year Summits/Events/Sports/IR/Inventions capsule + daily in-scope headlines (dated PDF) - auto commits & pushes to git." },
    @{ Name = "DailyPoliticalReforms";     Bat = "Static-GK\run_political_reforms.bat";         Offset = 30; Desc = "Political Reforms & Reformers: curated CM/minister/reformer capsule + daily political headlines tagged by state (dated PDF) - auto commits & pushes to git." },
    @{ Name = "DailyCommitPush";           Bat = "run_commit_push.bat";                          Offset = 45; Desc = "End-of-day sweep: stages ALL daily-generated changes, commits with a dated message, and pushes to origin/main (unattended)." }
)

function Remove-Task($name) {
    $existing = Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
    if ($existing) {
        Unregister-ScheduledTask -TaskName $name -Confirm:$false
        Write-Host "  Removed task '$name'." -ForegroundColor Yellow
    }
}

if ($Remove) {
    Write-Host "Removing all daily study tasks..." -ForegroundColor Cyan
    foreach ($t in $Tasks) { Remove-Task $t.Name }
    Write-Host "Done. All tasks removed." -ForegroundColor Green
    return
}

# Parse base time once, derive each task's time by adding its offset.
try {
    $baseDt = [DateTime]::ParseExact($BaseTime, "HH:mm", $null)
} catch {
    Write-Error "BaseTime must be HH:mm (24-hour), e.g. 07:00. Got '$BaseTime'."
    exit 1
}

Write-Host "Registering daily study tasks (base $BaseTime) in:" -ForegroundColor Cyan
Write-Host "  $Root`n"

foreach ($t in $Tasks) {
    $bat = Join-Path $Root $t.Bat
    if (-not (Test-Path $bat)) {
        Write-Warning "  Launcher missing, skipping '$($t.Name)': $bat"
        continue
    }
    $time = $baseDt.AddMinutes($t.Offset).ToString("HH:mm")
    $dir  = Split-Path -Parent $bat

    Remove-Task $t.Name   # idempotent re-install

    $Action  = New-ScheduledTaskAction -Execute $bat -WorkingDirectory $dir
    $Trigger = New-ScheduledTaskTrigger -Daily -At $time
    $Settings = New-ScheduledTaskSettingsSet `
        -StartWhenAvailable `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
        -RestartCount 2 `
        -RestartInterval (New-TimeSpan -Minutes 5)
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

    Register-ScheduledTask `
        -TaskName $t.Name `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Principal $Principal `
        -Description $t.Desc | Out-Null

    Write-Host ("  [OK] {0,-28} daily at {1}" -f $t.Name, $time) -ForegroundColor Green
}

Write-Host ""
Write-Host "All set. Check status with:" -ForegroundColor Cyan
Write-Host "    Get-ScheduledTask -TaskName DailyEditorialVocabulary,DailyOneWordSubstitution,DailyGKCurrentAffairs | Select TaskName,State"
Write-Host ""
Write-Host "Run one now (test):" -ForegroundColor Cyan
Write-Host "    Start-ScheduledTask -TaskName DailyGKCurrentAffairs"
Write-Host ""
Write-Host "Remove all later:" -ForegroundColor Cyan
Write-Host "    powershell -ExecutionPolicy Bypass -File .\setup_daily_tasks.ps1 -Remove"
