**OpenedFilesView.exe** (NirSoft)
Purpose: Show all files currently opened by processes on the system.
Flags: `/stext .\ofv_out.txt` | `/scsv .\ofv_out.csv`
Output: Tab-delimited or CSV when exported.
Chaining: First step in file-lock triage; feeds process name/PID to `handle64`.
Example: `.\nirsoft\OpenedFilesView.exe /stext .\ofv_out.txt`

