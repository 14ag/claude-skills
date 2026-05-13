**Procmon64.exe** [ADMIN][DRIVER]
Purpose: Real-time file system, registry, and process/thread activity monitor.
Flags: `/accepteula /quiet /minimized /backingfile .\procmon.pml /runtime 30`
Output: Binary PML file. Requires GUI or post-processing to read. Save path and report it.
Prerequisites: Admin required. Loads kernel driver on first run; unload on exit.
Chaining: Use after `handle64` or `OpenedFilesView` to capture live activity on a suspect path.
Example: `.\systeminternals\Procmon64.exe /accepteula /quiet /minimized /backingfile .\capture.pml /runtime 30`

