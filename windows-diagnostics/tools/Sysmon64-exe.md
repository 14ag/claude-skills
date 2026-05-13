**Sysmon64.exe** [ADMIN][DRIVER]
Purpose: Log detailed process creation, network, file, and registry events to the Windows Event Log.
Flags: `-accepteula -i <config.xml>` (install) | `-u` (uninstall) | `-c <config.xml>` (update config)
Output: Events written to `Microsoft-Windows-Sysmon/Operational` event log. Read with `psloglist64`.
Prerequisites: Admin required. Loads kernel driver; unload with `-u` on exit.
Chaining: Precedes `psloglist64` to collect structured event data.
Example: `.\systeminternals\Sysmon64.exe -accepteula -i .\sysmon_config.xml`

