**procdump64.exe** [ADMIN]
Purpose: Capture process memory dumps on trigger conditions (CPU spike, crash, hang).
Flags: `-accepteula -ma <PID> .\dump.dmp` | `-e` (on crash) | `-h` (on hang) | `-c <cpu%>` (CPU threshold)
Output: Binary DMP file at specified path.
Prerequisites: Admin for full dump of protected processes.
Chaining: Follows `pslist64` or `vmmap64` to identify suspect PID.
Example: `.\systeminternals\procdump64.exe -accepteula -ma 1234 .\proc1234.dmp`

