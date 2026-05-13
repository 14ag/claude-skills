**junction64.exe** [ADMIN]
Purpose: Create, list, or delete NTFS junction points (directory symlinks).
Flags: `-accepteula -s <path>` (list junctions recursively) | `<junction> <target>` (create)
Output: Plain text.
Example: `.\systeminternals\junction64.exe -accepteula -s C:\ | findstr /V "^$"`

