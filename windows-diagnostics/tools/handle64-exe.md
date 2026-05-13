**handle64.exe** [ADMIN][DRIVER]
Purpose: Show open file, registry, and object handles for all or specific processes.
Flags: `-accepteula` | `-p <PID|name>` | `-a` (all handle types) | `<path>` (filter by path)
Output: Plain text. Each line: `<process> pid: <PID> type: <type> <handle>: <path>`
Prerequisites: Admin required. Loads kernel driver.
Chaining: Follows `OpenedFilesView` to confirm locking process; feeds PID to `procexp64`.
Example: `.\systeminternals\handle64.exe -accepteula "C:\locked\file.txt" | findstr /V "^$"`

