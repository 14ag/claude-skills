# LoadOrdC64 - Load Order Console (64-bit)

## Purpose
Console version of LoadOrd that displays the order in which drivers and services are loaded at boot time. Useful for troubleshooting boot issues, driver conflicts, or understanding system startup sequence. Designed for scripting and automation.

## Syntax
```powershell
./systeminternals/LoadOrdC64.exe [-accepteula]
```

## Key Flags
- `-accepteula` - Accept EULA automatically (required for first run)

## Output Format
Plain text output with boot load order:
```
Load Order  Group                    Driver/Service Name
----------  -----------------------  -------------------
1           Boot Bus Extender        acpi
2           Boot Bus Extender        pci
3           System Bus Extender      isapnp
...
```

Columns:
- Load Order - Numeric sequence (1, 2, 3, ...)
- Group - Service group name (e.g., "Boot Bus Extender", "System Bus Extender")
- Driver/Service Name - Name of the driver or service

## Prerequisites
- [ADMIN] - Requires administrator privileges to query service database
- Console tool (suitable for scripting)

## Examples
```powershell
# Display boot load order
./systeminternals/LoadOrdC64.exe -accepteula

# Save load order to file
./systeminternals/LoadOrdC64.exe -accepteula > ./boot_load_order.txt

# Find when a specific driver loads
./systeminternals/LoadOrdC64.exe -accepteula | Select-String "disk"

# Compare load order before and after driver installation
./systeminternals/LoadOrdC64.exe -accepteula > ./load_order_before.txt
# Install driver
./systeminternals/LoadOrdC64.exe -accepteula > ./load_order_after.txt
Compare-Object (Get-Content ./load_order_before.txt) (Get-Content ./load_order_after.txt)
```

## Chaining Notes
- Use with: DriverView.exe (to see loaded drivers), PsService64.exe (to manage services)
- Output to: Text file for comparison or analysis
- Parse with: PowerShell Select-String or Compare-Object

## Error Handling
- Tool not found: Check if LoadOrdC64.exe exists in ./systeminternals/
- Access denied: Requires administrator privileges (relaunch shell as administrator)
- Empty output: Service database may be corrupted or inaccessible

## Common Use Cases
1. **Troubleshoot boot issues**: Identify which driver loads before a problematic driver
2. **Driver conflict analysis**: Check load order of conflicting drivers
3. **System startup audit**: Document boot sequence for compliance or documentation
4. **Before/after comparison**: Compare load order before and after driver installation

## Comparison with LoadOrd64.exe
- LoadOrd64.exe: GUI version with interactive sorting and filtering
- LoadOrdC64.exe: Console version for scripting and automation
- Both provide the same information, choose based on use case
