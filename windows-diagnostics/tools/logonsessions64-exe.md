**logonsessions64.exe** [ADMIN]
Purpose: List active logon sessions and the processes running in each.
Flags: `-accepteula` | `-p` (include processes)
Output: Plain text blocks per session.
Chaining: Follows `ADInsight64` in AD auth triage.
Example: `.\systeminternals\logonsessions64.exe -accepteula -p | findstr /V "^$"`

