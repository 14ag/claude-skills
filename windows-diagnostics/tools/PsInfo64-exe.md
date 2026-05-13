**PsInfo64.exe** [ADMIN]
Purpose: Display system information (OS version, uptime, CPU, RAM, hotfixes).
Flags: `-accepteula` | `\\<remote>` for remote system | `-s` (software installed) | `-h` (hotfixes)
Output: Plain text key-value pairs.
Chaining: First step in remote triage; precedes `PsService64` and `PsExec64`.
Example: `.\systeminternals\PsInfo64.exe -accepteula -s -h | findstr /V "^$"`

