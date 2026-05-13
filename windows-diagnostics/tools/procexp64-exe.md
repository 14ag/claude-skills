**procexp64.exe** [ADMIN]
Purpose: Interactive process explorer with full process tree, DLL, and handle detail.
Flags: `/accepteula` (suppress EULA on first run). GUI-only — no CLI export mode.
Output: GUI-only. Do not attempt to parse. Tell the user what to look for.
Prerequisites: Admin recommended for full handle/DLL visibility.
Chaining: Follow `pslist64` or `handle64` to confirm findings visually.
Example: `.\systeminternals\procexp64.exe /accepteula`

