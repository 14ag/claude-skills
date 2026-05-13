**RAMMap64.exe** [ADMIN]
Purpose: Physical memory usage breakdown by type (file, heap, standby, etc.).
Flags: `/accepteula`. GUI-only — no CLI export.
Output: GUI-only. Report path and instruct user to review.
Prerequisites: Admin required.
Chaining: Precedes `vmmap64` to identify which PID to investigate.
Example: `.\systeminternals\RAMMap64.exe /accepteula`

