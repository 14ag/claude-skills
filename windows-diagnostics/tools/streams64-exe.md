**streams64.exe**
Purpose: List or delete NTFS alternate data streams on files or directories.
Flags: `-accepteula -s <path>` (recurse) | `-d` (delete streams — DESTRUCTIVE)
Output: Plain text, one stream per line.
Chaining: Use after `sigcheck64` on a suspicious file to check for hidden payloads.
Example: `.\systeminternals\streams64.exe -accepteula -s C:\Downloads | findstr /V "^$"`

