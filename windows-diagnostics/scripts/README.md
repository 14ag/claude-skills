# Windows Diagnostics Utility Scripts

Automation scripts for common diagnostic workflows using Sysinternals and NirSoft tools.

## Available Scripts

### find_file_lock.ps1
Automates file lock investigation (Recipe a from SKILL.md).

**Usage**:
```powershell
.\scripts\find_file_lock.ps1 -FilePath "C:\path\to\locked\file.txt"
```

**What it does**:
1. Uses OpenedFilesView.exe to find processes with file open
2. Confirms with handle64.exe
3. Launches Process Explorer for visual confirmation

**Requirements**: Administrator privileges recommended

---

### triage_network.ps1
Automates network connection triage (Recipe b from SKILL.md).

**Usage**:
```powershell
.\scripts\triage_network.ps1 -RemoteIP "203.0.113.42"
```

**What it does**:
1. Lists all connections with tcpvcon64.exe
2. Performs WHOIS lookup on remote IP
3. Verifies owning process signature with sigcheck64.exe
4. Launches NetworkTrafficView for traffic capture

**Requirements**: Administrator privileges, internet connection for WHOIS and VirusTotal

**Warning**: Captures network traffic which may contain credentials

---

### memory_leak_check.ps1
Automates memory leak investigation (Recipe c from SKILL.md).

**Usage**:
```powershell
# Interactive mode (will prompt for PID)
.\scripts\memory_leak_check.ps1

# Direct mode (if you already know the PID)
.\scripts\memory_leak_check.ps1 -PID 1234
```

**What it does**:
1. Launches RAMMap64.exe to identify memory consumers
2. Launches vmmap64.exe to inspect process memory layout
3. Optionally captures memory dump with procdump64.exe

**Requirements**: Administrator privileges (mandatory)

**Output**: Creates `memleak_<PID>.dmp` file for analysis with WinDbg or Visual Studio

---

## General Notes

- All scripts require tools to be present in `./systeminternals/` and `./nirsoft/` directories
- Scripts validate tool availability and provide fallback suggestions
- Error handling includes validation of output files and tool exit codes
- All scripts use Unix-style paths (`./`) for cross-platform compatibility

## Prerequisites

- PowerShell 5.1 or later
- Administrator privileges (recommended for most scripts)
- Sysinternals Suite in `./systeminternals/`
- NirSoft utilities in `./nirsoft/`

## Troubleshooting

**"Tool not found" errors**:
- Verify tools are in correct directories
- Check if 32-bit variant exists (e.g., `procexp.exe` instead of `procexp64.exe`)

**"Access denied" errors**:
- Relaunch PowerShell as administrator
- Check if another instance of the tool is running

**"Output file not created" errors**:
- Verify shell is elevated
- Check disk space
- Ensure antivirus is not blocking tool execution
