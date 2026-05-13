**Autoruns64.exe** [ADMIN]
Purpose: GUI view of all autostart locations across the system.
Flags: `/accepteula`. GUI-only for interactive use; use `autorunsc64` for CLI.
Output: GUI-only. Use File > Save to export as `.arn` file.
Chaining: Precedes `sigcheck64` and `strings64` on flagged entries.
Example: `.\systeminternals\Autoruns64.exe /accepteula`

