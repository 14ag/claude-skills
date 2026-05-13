**sigcheck64.exe**
Purpose: Verify file signatures, check VirusTotal, and display version info.
Flags: `-accepteula` | `-u` (unsigned only) | `-v` (VirusTotal) | `-vt` (accept VT ToS) | `-s` (recurse) | `-c` (CSV)
Output: Plain text or CSV. Columns: File, Verified, Date, Publisher, Company, Description, Product, Prod version, File version, MachineType.
Chaining: Follows `autorunsc64`, `tcpvcon64`, or `Listdlls` to verify binaries.
Example: `.\systeminternals\sigcheck64.exe -accepteula -u -v C:\Windows\System32 | findstr /V "^$"`

