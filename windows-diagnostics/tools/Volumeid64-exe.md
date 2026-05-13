# Volumeid64.exe - Volume ID Changer

## Purpose
Change the volume ID (serial number) of FAT and NTFS volumes. Useful for disk imaging, system deployment, and resolving volume ID conflicts.

## Syntax
```powershell
./systeminternals/Volumeid64.exe [drive:] [new_id]
```

## Key Flags
- `drive:` - Target drive letter (e.g., C:, D:)
- `new_id` - New volume ID in hexadecimal format (8 characters)
- No flags - Display current volume ID

## Output Format
Displays current volume ID and confirms changes.

## Prerequisites
- **[ADMIN]** - Requires administrator privileges
- **[DESTRUCTIVE]** - Modifies volume metadata permanently
- Volume must not be in use by system processes

## Examples
```powershell
# Display current volume ID
./systeminternals/Volumeid64.exe C:

# Change volume ID to specific value
./systeminternals/Volumeid64.exe C: 12AB-34CD

# Display volume ID for multiple drives
./systeminternals/Volumeid64.exe D:
./systeminternals/Volumeid64.exe E:
```

## Use Cases
- **System deployment**: Ensure unique volume IDs across cloned systems
- **Disk imaging**: Prepare volumes for imaging operations
- **Conflict resolution**: Fix duplicate volume ID issues
- **Forensics**: Modify volume IDs for analysis isolation

## Chaining Notes
- **Use with**: disk2vhd64.exe (before creating VHD), du64.exe (disk analysis)
- **Output to**: Console display only
- **Parse with**: Text parsing for current ID extraction

## Error Handling
- **Tool not found**: Check for 32-bit variant (Volumeid.exe)
- **Access denied**: Requires administrator privileges
- **Volume in use**: Stop services or processes using the volume
- **Invalid format**: Volume ID must be 8 hexadecimal characters
- **Unsupported filesystem**: Only works with FAT and NTFS volumes

## Safety Notes
- **ALWAYS backup** volume before changing ID
- **Test on non-critical** volumes first
- **Document original** volume ID for recovery
- **Verify applications** don't depend on specific volume IDs

## Related Tools
- **disk2vhd64.exe** - Create volume snapshots before ID changes
- **ntfsinfo64.exe** - Display NTFS volume information
- **diskext64.exe** - Show volume extent information