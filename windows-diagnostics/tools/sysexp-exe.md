# sysexp - System Explorer

## Purpose
Comprehensive system information viewer that displays processes, modules, windows, services, drivers, and network connections in a unified interface. Alternative to Process Explorer with additional system-wide views.

## Syntax
```powershell
./nirsoft/sysexp.exe [/stext <output_file>] [/scsv <output_file>]
```

## Key Flags
- `/stext <file>` - Export current view to tab-delimited text file
- `/scsv <file>` - Export current view to CSV file
- `/shtml <file>` - Export current view to HTML file

## Output Format
Tab-delimited or CSV with columns (varies by view):

**Process View**:
- Process Name, PID, Parent PID, Threads, Handles, CPU Time, Memory Usage, Path

**Module View**:
- Module Name, Base Address, Size, Version, Company, Description, Path

**Window View**:
- Window Title, Class Name, Handle, Process Name, PID, Visible, Position

**Service View**:
- Service Name, Display Name, Status, Startup Type, Path, Description

## Prerequisites
- [ADMIN] - Some views require administrator privileges
- GUI tool (use `/stext` or `/scsv` for automation)

## Examples
```powershell
# Launch System Explorer GUI
./nirsoft/sysexp.exe

# Export current view to text file (must be done from GUI)
# File > Save Selected Items > Text File

# Alternative: Use specialized tools for specific views
# For processes: ProcessActivityView.exe
# For modules: Listdlls.exe
# For services: PsService64.exe
```

## Chaining Notes
- Use with: procexp64.exe (for detailed process analysis), DriverView.exe (for driver details)
- Output to: Text or CSV for parsing
- Parse with: PowerShell Import-Csv or Select-String
- Alternative: Use specialized tools (ProcessActivityView, Listdlls, PsService64) for better automation

## Error Handling
- Tool not found: Check if sysexp.exe exists in ./nirsoft/
- Access denied: Some views require administrator privileges (relaunch as administrator)
- GUI-only limitations: For automation, prefer specialized CLI tools

## Common Use Cases
1. **System overview**: Get unified view of processes, services, and drivers
2. **Process investigation**: View process tree with loaded modules and windows
3. **Service management**: Check service status and configuration
4. **Window enumeration**: Find hidden or background windows by process

## Notes
- Primarily a GUI tool with limited CLI automation
- For scripting, prefer specialized tools:
  - Processes: pslist64.exe, ProcessActivityView.exe
  - Modules: Listdlls.exe
  - Services: PsService64.exe
  - Windows: Use PowerShell Get-Process with MainWindowTitle
