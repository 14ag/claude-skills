# CPUSTRES64.exe - CPU Stress Testing Tool

## Purpose
Stress CPU threads to test thermal and stability limits. Useful for verifying cooling solutions, testing system stability under load, or reproducing thermal-related issues.

## Syntax
```powershell
./systeminternals/CPUSTRES64.exe
```

## Key Flags
- GUI-only tool (no command-line flags)
- Interactive thread and activity level selection

## Output Format
GUI-only. No file output. Monitor system behavior visually.

## Prerequisites
- [ADMIN] - Recommended for accurate CPU stress testing
- [DESTRUCTIVE] - Can cause system instability, thermal throttling, or crashes
- Requires explicit user confirmation before running
- Ensure adequate cooling and monitor temperatures

## Examples
```powershell
# NEVER run without explicit user confirmation
Write-Warning "CPUSTRES64 will stress CPU cores. This may cause system instability, thermal throttling, or crashes."
Write-Warning "Ensure adequate cooling and monitor temperatures during test."
$confirm = Read-Host "Proceed with CPU stress test? (y/n)"

if ($confirm -eq 'y') {
    ./systeminternals/CPUSTRES64.exe
    # In GUI: Set thread count and activity level, then click 'Start'
}
```

## Chaining Notes
- Use with: Coreinfo64.exe (to see CPU topology), Clockres64.exe (to measure timer resolution), dbgview64.exe (to watch for thermal messages)
- Output to: None (GUI-only monitoring)
- Parse with: N/A (visual monitoring only)

## Error Handling
- Tool not found: Check if CPUSTRES64.exe exists in ./systeminternals/
- System instability: Stop stress test immediately if system becomes unresponsive
- Thermal throttling: Monitor CPU temperature and reduce load if throttling occurs
- Crashes: Expected behavior for stability testing - verify crash dump configuration

## Common Use Cases
1. **Test cooling solution**: Verify CPU cooler can handle sustained load
2. **Stability testing**: Reproduce thermal-related crashes or instability
3. **Overclocking validation**: Test system stability after overclocking
4. **Thermal monitoring**: Identify thermal throttling thresholds

## CRITICAL WARNINGS
- **CAN CAUSE SYSTEM INSTABILITY** - Only use in controlled test environments
- **MONITOR TEMPERATURES** - Can cause thermal damage if cooling is inadequate
- **SAVE ALL WORK** before running
- **NOT FOR PRODUCTION SYSTEMS** - Use only in test/lab environments
- **CONFIRM WITH USER** before executing

## See Also
- CHM Help: `hh.exe ./systeminternals/Pstools.chm` (general Sysinternals documentation)
- Related tools: Coreinfo64.exe, Clockres64.exe, dbgview64.exe
