# RegDllView - Registered DLL/OCX/ActiveX Viewer

## Purpose
Display all registered DLL, OCX, and ActiveX files in the Windows registry. Useful for troubleshooting COM registration issues, identifying orphaned registrations, or auditing installed components.

## Syntax
```powershell
./nirsoft/RegDllView.exe [/stext <output_file>] [/scsv <output_file>]
```

## Key Flags
- `/stext <file>` - Export results to tab-delimited text file
- `/scsv <file>` - Export results to CSV file
- `/shtml <file>` - Export results to HTML file
- `/sort <column>` - Sort by column name (e.g., "Filename", "Description")

## Output Format
Tab-delimited or CSV with columns:
- Filename - Full path to the DLL/OCX/ActiveX file
- Description - File description from version info
- File Version - Version number of the file
- Product Name - Product name from version info
- Company - Company name from version info
- File Size - Size of the file in bytes
- File Time - Last modification time
- CLSID - COM Class ID
- ProgID - Programmatic identifier
- File Exists - Yes/No indicator if file still exists on disk

## Prerequisites
- No special privileges required
- GUI tool (use `/stext` or `/scsv` for automation)

## Examples
```powershell
# Export all registered DLLs to text file
./nirsoft/RegDllView.exe /stext ./regdll_list.txt

# Export to CSV for analysis
./nirsoft/RegDllView.exe /scsv ./regdll_list.csv

# Find orphaned registrations (files that no longer exist)
./nirsoft/RegDllView.exe /stext ./regdll_list.txt
Select-String -Path ./regdll_list.txt -Pattern "File Exists.*No"
```

## Chaining Notes
- Use with: dllexp.exe (to inspect exported functions), sigcheck64.exe (to verify signatures)
- Output to: Text or CSV for parsing
- Parse with: PowerShell Import-Csv or Select-String

## Error Handling
- Tool not found: Check if RegDllView.exe exists in ./nirsoft/
- Empty output: May indicate registry corruption or no registered components
- Access denied: Some registry keys may require elevation (relaunch as administrator)

## Common Use Cases
1. **Find orphaned COM registrations**: Export list and filter for "File Exists: No"
2. **Audit installed components**: Review all registered DLLs for security assessment
3. **Troubleshoot COM errors**: Verify if required DLL is registered and file exists
4. **Identify unsigned components**: Chain with sigcheck64 to verify signatures
