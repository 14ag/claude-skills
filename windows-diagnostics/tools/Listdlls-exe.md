**Listdlls.exe**
Purpose: List DLLs loaded by processes, including unsigned or unsigned-path DLLs.
Flags: `-accepteula` | `-u` (unsigned only) | `<process name>` | `-d <dll name>`
Output: Plain text. Skip header block up to first blank line.
Chaining: Follows `pslist64`; feeds DLL paths to `sigcheck64`.
Example: `.\systeminternals\Listdlls.exe -accepteula -u | findstr /V "^$"`

