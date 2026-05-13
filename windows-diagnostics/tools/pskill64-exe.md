**pskill64.exe** [DESTRUCTIVE]
Purpose: Terminate a process by name or PID.
Flags: `-accepteula <PID|name>` | `-t` (kill process tree)
Output: Plain text confirmation.
Prerequisites: Requires explicit user confirmation before running.
Chaining: Follows `pslist64` to confirm PID.
Example: `.\systeminternals\pskill64.exe -accepteula 1234`

