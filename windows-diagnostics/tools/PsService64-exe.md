**PsService64.exe** [ADMIN]
Purpose: View and control services on local or remote systems.
Flags: `-accepteula` | `query <service>` | `start <service>` | `stop <service>` | `\\<remote>`
Output: Plain text service status blocks.
Chaining: Follows `PsInfo64`; precedes `PsExec64` for remediation.
Example: `.\systeminternals\PsService64.exe -accepteula \\REMOTEPC query RemoteRegistry`

