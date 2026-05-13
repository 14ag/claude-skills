**movefile64.exe** [DESTRUCTIVE]
Purpose: Schedule a file move or delete to occur at next reboot.
Flags: `-accepteula <source> <destination>` | leave destination empty to schedule delete
Prerequisites: Explicit user confirmation required.
Output: Plain text confirmation.
Example: `.\systeminternals\movefile64.exe -accepteula C:\locked.dll ""` (confirm first)

