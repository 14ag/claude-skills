**tcpvcon64.exe** [ADMIN]
Purpose: List active TCP and UDP connections with owning process.
Flags: `-accepteula -a` (all connections) | `-c` (CSV output) | `-n` (no DNS resolution)
Output: CSV with columns: Protocol, Local Address, Local Port, Remote Address, Remote Port, State, PID, Process Name.
Chaining: Feeds remote IP to `whois64`; feeds PID to `sigcheck64` on the process binary.
Example: `.\systeminternals\tcpvcon64.exe -accepteula -a -c | findstr /V "^$"`

