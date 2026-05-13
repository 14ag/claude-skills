**vmmap64.exe** [ADMIN]
Purpose: Visualise virtual memory layout of a process.
Flags: `-accepteula <PID>` for CLI snapshot export.
Output: GUI-only for interactive use. CLI mode exports XML to stdout.
Prerequisites: Admin for full access to protected processes.
Chaining: Follows `RAMMap64` to drill into a suspect PID.
Example: `.\systeminternals\vmmap64.exe -accepteula 1234`

