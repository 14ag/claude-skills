**DriverView.exe** (NirSoft)
Purpose: List all loaded kernel drivers with version and path info.
Flags: `/stext .\driverview_out.txt`
Output: Tab-delimited text when exported.
Chaining: Use after `sigcheck64` to check driver signatures.
Example: `.\nirsoft\DriverView.exe /stext .\driverview_out.txt`

