param(
    [string]$TaskName = "WikiMemoryRefresh",
    [string]$ProjectRoot = (Resolve-Path ".").Path,
    [string]$PythonExe = "python"
)

# Prepared only. Review this file before running it to activate the scheduler.
# Allowed weekdays: monday, tuesday, wednesday, thursday, friday
# Local run time: 09:00
# Refresh command: python -m wikimemory memory-refresh --consumer-profile-extraction-model gpt-4o-mini --consumer-profile-merge-model gpt-5.3-codex --consumer-profile-window-max-chars 60000

$action = New-ScheduledTaskAction `
    -Execute $PythonExe `
    -Argument "-m wikimemory memory-refresh --consumer-profile-extraction-model gpt-4o-mini --consumer-profile-merge-model gpt-5.3-codex --consumer-profile-window-max-chars 60000" `
    -WorkingDirectory $ProjectRoot

$trigger = New-ScheduledTaskTrigger `
    -Weekly `
    -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday `
    -At ([datetime]::Today.AddHours(9).AddMinutes(0))

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -MultipleInstances IgnoreNew

# Register-ScheduledTask `
#     -TaskName $TaskName `
#     -Action $action `
#     -Trigger $trigger `
#     -Settings $settings `
#     -Description "Run WikiMemory memory refresh based on prepared scheduler policy."

# Write-Host "Prepared scheduler activation script. Uncomment Register-ScheduledTask when you want to activate it."
