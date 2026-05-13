**du64.exe**
Purpose: Report disk usage for a directory tree.
Flags: `-accepteula -l <depth>` | `-q` (quiet, no banner) | `<path>`
Output: Plain text. Final line shows total bytes.
Chaining: Use before `Disk2vhd` to estimate image size.
Example: `.\systeminternals\du64.exe -accepteula -q -l 2 C:\Users`

