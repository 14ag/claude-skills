**psping64.exe**
Purpose: Measure TCP/UDP latency and bandwidth; ICMP ping with statistics.
Flags: `-accepteula <host>:<port>` | `-u` (UDP) | `-b` (bandwidth test) | `-n <count>`
Output: Plain text statistics block.
Chaining: Use after `tcpvcon64` to test reachability of a flagged remote address.
Example: `.\systeminternals\psping64.exe -accepteula -n 10 8.8.8.8:443`

