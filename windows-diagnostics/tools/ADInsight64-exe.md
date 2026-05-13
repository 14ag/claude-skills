**ADInsight64.exe** [ADMIN]
Purpose: Real-time LDAP traffic analyser — captures all LDAP calls from client applications.
Flags: `/accepteula`. GUI-only.
Output: GUI-only. Use File > Save to export trace.
Chaining: First step in AD auth triage; feeds findings to `psloglist64` and `logonsessions64`.
Example: `.\systeminternals\ADInsight64.exe /accepteula`

