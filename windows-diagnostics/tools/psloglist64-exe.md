**psloglist64.exe** [ADMIN]
Purpose: Dump Windows event log entries from local or remote systems.
Flags: `-accepteula` | `-s` (Security log) | `-a <date>` (after date) | `-x` (extended info) | `-c` (clear log after dump) | `\\<remote>`
Output: Plain text, one event per block. Skip header lines.
Chaining: Follows `Sysmon64` or `ADInsight64` to retrieve logged events.
Example: `.\systeminternals\psloglist64.exe -accepteula -s | findstr /V "^$"`


### G. Remote & Admin Operations

