**PsExec64.exe** [ADMIN]
Purpose: Execute processes on remote systems with optional interactive session.
Flags: `-accepteula \\<remote> -u <user> -p <pass> <command>` | `-s` (run as SYSTEM) | `-i` (interactive) | `-d` (don't wait)
Output: Stdout/stderr of the remote command piped back locally.
Chaining: Follows `PsInfo64` and `PsService64` in remote triage.
Example: `.\systeminternals\PsExec64.exe -accepteula \\REMOTEPC -s ipconfig /all`

