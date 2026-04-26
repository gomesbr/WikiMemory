param(
    [string]$TaskName = "WikiMemoryRefresh",
    [string]$ProjectRoot = (Resolve-Path ".").Path,
    [string]$PythonExe = "python",
    [string]$IntervalMinutes = "60",
    [switch]$Activate
)

$action = New-ScheduledTaskAction `
    -Execute $PythonExe `
    -Argument "-m wikimemory memory-refresh" `
    -WorkingDirectory $ProjectRoot

$trigger = New-ScheduledTaskTrigger `
    -Once `
    -At (Get-Date).AddMinutes(1) `
    -RepetitionInterval (New-TimeSpan -Minutes ([int]$IntervalMinutes))

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -MultipleInstances IgnoreNew

if (-not $Activate) {
    Write-Host "Prepared scheduled-task objects only. Re-run with -Activate when you want to register the task."
    Write-Host "TaskName: $TaskName"
    Write-Host "ProjectRoot: $ProjectRoot"
    Write-Host "PythonExe: $PythonExe"
    Write-Host "IntervalMinutes: $IntervalMinutes"
    return
}

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Run WikiMemory incremental memory refresh."
