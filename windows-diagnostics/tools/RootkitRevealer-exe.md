# RootkitRevealer.exe - Rootkit Detection Tool

## Purpose
Advanced rootkit detection tool that compares registry and file system APIs to detect discrepancies that indicate rootkit presence. Identifies hidden files, processes, and registry keys.

## Syntax
```powershell
./systeminternals/RootkitRevealer.exe [options]
```

## Key Features
- **API comparison**: Compares high-level and low-level API results
- **Registry scanning**: Detects hidden registry keys and values
- **File system scanning**: Identifies hidden files and directories
- **Process detection**: Finds hidden processes and threads
- **Heuristic analysis**: Uses multiple detection techniques
- **Detailed reporting**: Comprehensive scan results with explanations

## Prerequisites
- **[ADMIN]** - Requires administrator privileges
- **[DRIVER]** - Loads kernel-mode driver for low-level access
- GUI environment required (interactive tool)
- Significant system resources during scan

## Usage Scenarios
```powershell
# Launch RootkitRevealer for interactive scan
./systeminternals/RootkitRevealer.exe

# For automated scanning, use command-line options (if available)
# Note: Primarily a GUI tool - check documentation for CLI options
```

## Scan Process
1. **Initialization**: Loads kernel driver and prepares scan engines
2. **Registry scan**: Compares registry enumeration methods
3. **File system scan**: Compares file enumeration methods  
4. **Process scan**: Compares process enumeration methods
5. **Analysis**: Identifies discrepancies and potential rootkits
6. **Reporting**: Displays results with severity ratings

## Detection Methods
- **SSDT hooking detection**: Identifies system service table modifications
- **IRP hooking detection**: Finds I/O request packet interception
- **File system filter detection**: Locates file system filter drivers
- **Registry filter detection**: Identifies registry filtering mechanisms
- **Process hiding detection**: Finds hidden processes and threads

## Chaining Notes
- **Use with**: Autoruns64.exe (startup analysis), sigcheck64.exe (file verification), strings64.exe (malware analysis)
- **Output to**: GUI display with export options
- **Parse with**: Manual analysis of scan results

## Error Handling
- **Tool not found**: No 32-bit variant available (64-bit only)
- **Access denied**: Requires administrator privileges
- **Driver load failure**: May need system reboot or driver cleanup
- **Scan interruption**: Can resume or restart scan as needed
- **False positives**: Verify findings with additional tools

## Interpretation Guidelines
- **High confidence**: Multiple detection methods agree
- **Medium confidence**: Single detection method with strong indicators
- **Low confidence**: Weak indicators requiring further investigation
- **False positives**: Legitimate software with rootkit-like behavior

## Related Tools
- **Autoruns64.exe** - Analyze startup locations for persistence
- **sigcheck64.exe** - Verify digital signatures of suspicious files
- **strings64.exe** - Extract strings from suspicious binaries
- **ProcessActivityView.exe** - Monitor process behavior
- **Procmon64.exe** - Real-time system activity monitoring

## Advanced Usage
- **Baseline scanning**: Create clean system baseline for comparison
- **Targeted scanning**: Focus on specific areas of concern
- **Batch analysis**: Process multiple systems with similar configurations
- **Forensic analysis**: Preserve scan results for incident response