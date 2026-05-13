**pssuspend64.exe**
Purpose: Suspend or resume a process without terminating it.
Flags: `-accepteula <PID|name>` | `-r` (resume)
Output: Plain text confirmation.
Chaining: Use before `vmmap64` or `procdump64` to freeze state.
Example: `.\systeminternals\pssuspend64.exe -accepteula 1234`

