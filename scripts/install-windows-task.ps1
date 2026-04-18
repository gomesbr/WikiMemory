param(
    [string]$TaskName = "WikiMemoryRefresh",
    [string]$ProjectRoot = (Resolve-Path ".").Path,
    [string]$PythonExe = "python",
    [string]$IntervalMinutes = "60"
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

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Run WikiMemory incremental memory refresh."
