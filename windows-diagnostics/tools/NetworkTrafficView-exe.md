**NetworkTrafficView.exe** (NirSoft) [CAPTURE]
Purpose: Capture and display network traffic statistics per connection.
Flags: `/stext .\ntv_out.txt` to export summary.
Output: Tab-delimited text when exported.
Prerequisites: Admin recommended. Warn user that captured traffic may contain credentials.
Chaining: Follows `tcpvcon64` and `whois64` to capture traffic from a flagged connection.
Example: `.\nirsoft\NetworkTrafficView.exe /stext .\ntv_out.txt`

