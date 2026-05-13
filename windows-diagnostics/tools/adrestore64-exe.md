**adrestore64.exe** [ADMIN][DESTRUCTIVE]
Purpose: List and restore deleted Active Directory objects from the tombstone.
Flags: `-accepteula` | `-r <object name>` (restore — DESTRUCTIVE)
Prerequisites: Admin and domain connectivity required. Explicit user confirmation before `-r`.
Output: Plain text list of tombstoned objects.
Example: `.\systeminternals\adrestore64.exe -accepteula | findstr /V "^$"`



