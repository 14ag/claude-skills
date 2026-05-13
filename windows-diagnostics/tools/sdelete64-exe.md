**sdelete64.exe** [DESTRUCTIVE]
Purpose: Securely delete files or wipe free space.
Flags: `-accepteula -p <passes> <path>` | `-z` (zero free space) | `-c` (clean free space)
Prerequisites: Explicit user confirmation required. Irreversible.
Output: Plain text progress.
Example: `.\systeminternals\sdelete64.exe -accepteula -p 3 .\sensitive.txt` (confirm first)

