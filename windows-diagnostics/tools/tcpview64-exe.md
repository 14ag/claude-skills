# tcpview64.exe - GUI Network Connection Viewer

## Purpose
Interactive GUI tool to view active TCP and UDP connections with real-time updates. GUI version of tcpvcon64.exe with visual process tree and connection details.

## Syntax
```powershell
./systeminternals/tcpview64.exe [/accepteula]
```

## Key Features
- Real-time connection monitoring
- Process tree view with connection ownership
- Connection state visualization (established, listening, etc.)
- Right-click context menu for process termination
- Color-coded connection states
- Automatic refresh with configurable intervals

## Prerequisites
- **[ADMIN]** - Requires administrator privileges for full functionality
- GUI environment required (not suitable for headless/CLI scenarios)

## Usage Scenarios
```powershell
# Launch TCPView for interactive monitoring
./systeminternals/tcpview64.exe /accepteula

# For CLI scenarios, use tcpvcon64.exe instead
./systeminternals/tcpvcon64.exe -accepteula -a -c
```

## GUI Features
- **File Menu**: Save connection list, refresh options
- **View Menu**: Filter by protocol, process, state
- **Options Menu**: Auto-refresh settings, always on top
- **Context Menu**: Kill process, close connection, properties

## Chaining Notes
- **Use with**: tcpvcon64.exe (CLI equivalent), whois64.exe (IP lookup), sigcheck64.exe (process verification)
- **Output to**: Visual display only (no file export)
- **Parse with**: Manual observation (use tcpvcon64.exe for automated parsing)

## Error Handling
- **Tool not found**: Check for 32-bit variant (tcpview.exe)
- **Access denied**: Requires administrator privileges for process details
- **GUI not available**: Use tcpvcon64.exe for CLI scenarios

## Related Tools
- **tcpvcon64.exe** - CLI equivalent with CSV export
- **cports.exe** - NirSoft alternative with export options
- **NetworkTrafficView.exe** - Traffic statistics and capture