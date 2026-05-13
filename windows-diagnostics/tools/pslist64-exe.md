**pslist64.exe**
Purpose: List running processes with CPU and memory stats.
Flags: `-accepteula` | `-t` (tree view) | `-x` (include threads and DLLs) | `\\<remote>` for remote
Output: Plain text, one process per line. Skip header lines starting with `Name`.
Chaining: Feeds PID to `procdump64`, `vmmap64`, `pskill64`, `pssuspend64`.
Example: `.\systeminternals\pslist64.exe -accepteula -t | findstr /V "^$"`

