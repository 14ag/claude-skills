# notmyfaultc64 - Console Crash Testing Tool (64-bit)

## Purpose
Console version of notmyfault that deliberately crashes the system or causes resource leaks for testing crash dump configuration, kernel debugger setup, or system stability. Designed for scripting and automated testing.

## Syntax
```powershell
./systeminternals/notmyfaultc64.exe [-accepteula] <crash_type>
```

## Key Flags
- `-accepteula` - Accept EULA automatically (required for first run)

## Crash Types
- `crash` - Cause a kernel-mode crash (BSOD)
- `hang` - Hang the system (requires hard reset)
- `highlevel` - High IRQL crash
- `buffer` - Buffer overflow crash
- `hardlock` - Hard lock (requires hard reset)
- `stacktrash` - Stack trash crash
- `leak` - Leak kernel pool memory
- `memeater` - Consume all available memory

## Output Format
Minimal console output before crash:
```
Notmyfault v4.20 - Crash, hang and kernel pool leak tester
Copyright (C) 2002-2016 Mark Russinovich
Sysinternals - www.sysinternals.com

Crashing...
```

System will then crash or hang based on selected type.

## Prerequisites
- [ADMIN] - Requires administrator privileges
- [DRIVER] - Loads kernel driver (myfault.sys)
- [DESTRUCTIVE] - WILL CRASH OR HANG THE SYSTEM
- Console tool (suitable for scripting)

## Examples
```powershell
# NEVER run these without explicit user confirmation and understanding of consequences

# Test crash dump configuration (will cause BSOD)
Write-Warning "This will crash the system. Ensure all work is saved."
$confirm = Read-Host "Proceed? (y/n)"
if ($confirm -eq 'y') {
    ./systeminternals/notmyfaultc64.exe -accepteula crash
}

# Test memory leak detection (will consume memory until system is unstable)
Write-Warning "This will leak kernel memory. System may become unstable."
$confirm = Read-Host "Proceed? (y/n)"
if ($confirm -eq 'y') {
    ./systeminternals/notmyfaultc64.exe -accepteula leak
}
```

## Chaining Notes
- Use with: WinDbg (to analyze crash dumps), livekd64.exe (to debug live kernel)
- Output to: Crash dump file (configured in System Properties > Advanced > Startup and Recovery)
- Parse with: WinDbg !analyze -v command

## Error Handling
- Tool not found: Check if notmyfaultc64.exe exists in ./systeminternals/
- Access denied: Requires administrator privileges (relaunch shell as administrator)
- Driver load failure: Check if another instance is running or driver is stuck from previous crash

## Common Use Cases
1. **Test crash dump configuration**: Verify that crash dumps are being captured correctly
2. **Kernel debugger setup**: Test kernel debugger connection and symbol resolution
3. **System stability testing**: Verify system recovery after crash
4. **Memory leak detection**: Test memory leak detection tools and monitoring

## CRITICAL WARNINGS
- **WILL CRASH OR HANG THE SYSTEM** - Only use in controlled test environments
- **SAVE ALL WORK** before running any crash type
- **REQUIRES REBOOT** after most crash types
- **NOT FOR PRODUCTION SYSTEMS** - Use only in test/lab environments
- **CONFIRM WITH USER** before executing any crash command

## Comparison with notmyfault64.exe
- notmyfault64.exe: GUI version with interactive crash type selection
- notmyfaultc64.exe: Console version for scripting and automated testing
- Both cause the same crashes, choose based on use case
