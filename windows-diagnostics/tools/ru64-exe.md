**ru64.exe** [ADMIN]
Purpose: Show registry disk usage by key, useful for inventorying large hives.
Flags: `-accepteula <registry path>` | `-c` (CSV) | `-l <depth>`
Output: Plain text or CSV.
Chaining: Use in pre-change snapshot to inventory registry size.
Example: `.\systeminternals\ru64.exe -accepteula -c HKLM > .\reg_inventory.csv`


### E. System Info & Security

