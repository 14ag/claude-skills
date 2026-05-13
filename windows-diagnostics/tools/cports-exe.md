**cports.exe** (NirSoft)
Purpose: Display open TCP/UDP ports with process and module info.
Flags: `/stext .\cports_out.txt` | `/scsv .\cports_out.csv`
Output: Tab-delimited or CSV when exported.
Chaining: Alternative to `tcpvcon64`; feeds process path to `sigcheck64`.
Example: `.\nirsoft\cports.exe /scsv .\cports_out.csv`

