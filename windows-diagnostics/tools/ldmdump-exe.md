# ldmdump - Logical Disk Manager Database Dump

## Purpose
Dump the Logical Disk Manager (LDM) database information for dynamic disks. Useful for troubleshooting dynamic disk issues, recovering disk configuration, or understanding disk group membership.

## Syntax
```powershell
./systeminternals/ldmdump.exe [-accepteula]
```

## Key Flags
- `-accepteula` - Accept EULA automatically (required for first run)

## Output Format
Plain text output with LDM database information:
```
Logical Disk Manager Database Dump v1.02
Copyright (C) 2000-2016 Mark Russinovich
Sysinternals - www.sysinternals.com

Disk Group: Disk Group 1
  GUID: {12345678-1234-1234-1234-123456789012}
  
  Disks:
    Disk 1: PHYSICALDRIVE1
      GUID: {87654321-4321-4321-4321-210987654321}
      Size: 500 GB
      
  Volumes:
    Volume 1: E:
      Type: Simple
      Size: 500 GB
      Disk: Disk 1
```

Includes:
- Disk group names and GUIDs
- Physical disk information
- Volume configuration (simple, spanned, striped, mirrored, RAID-5)
- Disk and volume GUIDs
- Size information

## Prerequisites
- [ADMIN] - Requires administrator privileges to access LDM database
- Console tool (suitable for scripting)
- Only works with dynamic disks (not basic disks)

## Examples
```powershell
# Dump LDM database information
./systeminternals/ldmdump.exe -accepteula

# Save LDM database to file for documentation
./systeminternals/ldmdump.exe -accepteula > ./ldm_config.txt

# Check if system has dynamic disks
./systeminternals/ldmdump.exe -accepteula | Select-String "Disk Group"

# Document disk configuration before changes
./systeminternals/ldmdump.exe -accepteula > ./ldm_before.txt
# Make disk changes
./systeminternals/ldmdump.exe -accepteula > ./ldm_after.txt
Compare-Object (Get-Content ./ldm_before.txt) (Get-Content ./ldm_after.txt)
```

## Chaining Notes
- Use with: diskext64.exe (to see disk extents), DiskView64.exe (to visualize disk layout)
- Output to: Text file for documentation or comparison
- Parse with: PowerShell Select-String or regex matching

## Error Handling
- Tool not found: Check if ldmdump.exe exists in ./systeminternals/
- Access denied: Requires administrator privileges (relaunch shell as administrator)
- No output: System has no dynamic disks (only basic disks present)
- "Unable to open LDM database": LDM service may not be running or database is corrupted

## Common Use Cases
1. **Document dynamic disk configuration**: Save LDM database before making changes
2. **Troubleshoot disk group issues**: Verify disk group membership and volume configuration
3. **Recover disk configuration**: Use output to recreate disk configuration after failure
4. **Audit disk layout**: Document disk groups and volumes for compliance or inventory

## Notes
- Only works with dynamic disks (Windows 2000 and later)
- Basic disks do not have LDM database and will produce no output
- For basic disk information, use diskext64.exe or DiskView64.exe instead
- LDM database is stored in a reserved 1 MB region at the end of each dynamic disk
