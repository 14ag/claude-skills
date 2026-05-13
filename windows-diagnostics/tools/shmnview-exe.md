# shmnview - Shared Memory Viewer

## Purpose
Display all shared memory sections currently allocated on the system and the processes accessing them. Useful for investigating inter-process communication, memory leaks in shared memory, or identifying processes sharing data.

## Syntax
```powershell
./nirsoft/shmnview.exe [/stext <output_file>] [/scsv <output_file>]
```

## Key Flags
- `/stext <file>` - Export results to tab-delimited text file
- `/scsv <file>` - Export results to CSV file
- `/shtml <file>` - Export results to HTML file
- `/sort <column>` - Sort by column name (e.g., "Name", "Size")

## Output Format
Tab-delimited or CSV with columns:
- Name - Name of the shared memory section
- Size - Size of the shared memory section in bytes
- Process ID - PID of the process that created the section
- Process Name - Name of the process that created the section
- Process Path - Full path to the process executable
- Created Time - When the shared memory section was created
- Modified Time - Last modification time
- Access Count - Number of processes accessing this section

## Prerequisites
- [ADMIN] - Requires administrator privileges to view all shared memory sections
- GUI tool (use `/stext` or `/scsv` for automation)

## Examples
```powershell
# Export all shared memory sections to text file
./nirsoft/shmnview.exe /stext ./shmem_list.txt

# Export to CSV for analysis
./nirsoft/shmnview.exe /scsv ./shmem_list.csv

# Find large shared memory sections (potential memory leaks)
./nirsoft/shmnview.exe /stext ./shmem_list.txt
Select-String -Path ./shmem_list.txt -Pattern "Size.*[0-9]{8,}" | Select-Object -First 10

# Identify processes sharing memory
./nirsoft/shmnview.exe /scsv ./shmem_list.csv
Import-Csv ./shmem_list.csv | Group-Object Name | Where-Object { $_.Count -gt 1 }
```

## Chaining Notes
- Use with: ProcessActivityView.exe (to see process activity), vmmap64.exe (to inspect process memory layout)
- Output to: Text or CSV for parsing
- Parse with: PowerShell Import-Csv or Select-String

## Error Handling
- Tool not found: Check if shmnview.exe exists in ./nirsoft/
- Access denied: Requires administrator privileges (relaunch shell as administrator)
- Empty output: No shared memory sections currently allocated (normal on idle system)

## Common Use Cases
1. **Investigate IPC mechanisms**: Identify processes communicating via shared memory
2. **Find memory leaks**: Look for large or growing shared memory sections
3. **Security audit**: Identify sensitive data in shared memory
4. **Performance analysis**: Measure shared memory usage across processes
