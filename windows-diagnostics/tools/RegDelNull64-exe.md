**RegDelNull64.exe** [ADMIN][DESTRUCTIVE]
Purpose: Scan and optionally delete registry keys containing embedded null characters.
Flags: `-accepteula <hive path>` | `-s` (recurse) | `-c` (delete — DESTRUCTIVE)
Prerequisites: Admin required. Explicit user confirmation before using `-c`.
Output: Plain text list of found keys.
Example: `.\systeminternals\RegDelNull64.exe -accepteula -s HKLM | findstr /V "^$"`

