**psshutdown64.exe** [ADMIN][DESTRUCTIVE]
Purpose: Shut down, restart, or log off local or remote systems.
Flags: `-accepteula -s` (shutdown) | `-r` (restart) | `-t <seconds>` (delay) | `\\<remote>`
Prerequisites: Explicit user confirmation required.
Output: Plain text confirmation.
Example: `.\systeminternals\psshutdown64.exe -accepteula -r -t 60 \\REMOTEPC` (confirm first)

